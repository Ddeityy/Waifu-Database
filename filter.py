from django import setup
import json
import os
from tags import BAD_TAGS

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "filter_settings")
setup()
from db.models import *


# "tag_string_general":"1boy black_hair chocolate male_focus red_eyes shirt solo striped striped_shirt",
# "tag_string":"1boy black_hair chocolate ikari_shinji male_focus neon_genesis_evangelion red_eyes shirt solo striped striped_shirt",
# "preview_file_url":"https://cdn.donmai.us/preview/cd/89/cd89a5178b4c827a6e4cf052b7953d61.jpg",
# "large_file_url":"https://cdn.donmai.us/original/cd/89/cd89a5178b4c827a6e4cf052b7953d61.png",
# "tag_string_character":"ikari_shinji",
# "tag_count_copyright":"1",
# "is_deleted":true,
# "score":"0",
# "rating":"s",
# "tag_string_copyright":"neon_genesis_evangelion",
# "id":"460994",
# "tag_count_character":"1",


def waifu_exists(line):
    name = line["tag_string_character"].split(" ")[0]
    return Waifu.objects.filter(name=name).exists()


def update_scores(line):
    waifu_name = line["tag_string_character"].split(" ")[0]
    new_score = int(line["score"])
    if waifu_name == "":
        return False
    else:
        try:
            waifu = Waifu.objects.get(name=waifu_name)
            current_safe_score = waifu.best_safe_post_score
            current_unsafe_score = waifu.best_unsafe_post_score
            if line["rating"] == "s" and new_score > 0:
                waifu.best_safe_post_id = int(line["id"])
                waifu.best_safe_post_score = new_score
                waifu.best_safe_post_image = line["file_url"]
                if current_safe_score == None:
                    current_safe_score = new_score
                    waifu.save()
                else:
                    if current_safe_score < new_score:
                        current_safe_score = new_score
                        waifu.save()
            elif new_score > 0:
                waifu.best_unsafe_post_id = int(line["id"])
                waifu.best_unsafe_post_score = new_score
                waifu.best_unsafe_post_image = line["file_url"]
                if current_unsafe_score == None:
                    current_unsafe_score = new_score
                    waifu.save()
                else:
                    if current_unsafe_score < new_score:
                        current_unsafe_score = new_score
                        waifu.save()
        except KeyError or AttributeError or ValueError:
            pass


def check_tags(tags) -> bool:
    counter = 0
    for tag in tags:
        if tag in BAD_TAGS:
            counter += 1
    if counter > 0:
        return False
    else:
        return True


def filter(line):
    tags = line["tag_string"].split(" ")
    source_count = int(line["tag_count_copyright"])
    character_count = int(line["tag_count_character"])
    print(character_count)
    if character_count == 1 or 2:
        name = line["tag_string_character"].split(" ")[0]
        match source_count:
            case 0:
                print("Skipped: no source")
                return False
            case num if num in range(1, 3):
                if not check_tags(tags):
                    print("Skipped: bad tags")
                    return False
                elif ("solo" or "solo_focus") and "1girl" in tags:
                    if r"_(cosplay)" in name:
                        print("Skipped: cosplay")
                        return False
                    return True
                else:
                    return False
            case _:
                print("Skipped: too many sources")
                return False

    else:
        print("Skipped: too little/many characters")
        return False


def add_waifu(line):
    try:
        name = line["tag_string_character"].split(" ")[0]
        sources = line["tag_string_copyright"]
        if line["rating"] == "s":
            best_safe_post_id = int(line["id"])
            best_safe_post_score = int(line["score"])
            best_safe_post_image = line["large_file_url"]
            Waifu.objects.create(
                name=name,
                source=sources,
                best_safe_post_id=best_safe_post_id,
                best_safe_post_score=best_safe_post_score,
                best_safe_post_image=best_safe_post_image,
            )
            print(f"Added waifu: {name}")
        else:
            best_unsafe_post_id = int(line["id"])
            best_unsafe_post_score = int(line["score"])
            best_unsafe_post_image = line["large_file_url"]
            Waifu.objects.create(
                name=name,
                source=sources,
                best_unsafe_post_id=best_unsafe_post_id,
                best_unsafe_post_score=best_unsafe_post_score,
                best_unsafe_post_image=best_unsafe_post_image,
            )
            print(f"Added waifu: {name}")
    except KeyError or AttributeError or ValueError:
        print("Skipped: incomplete data")


def parse_tags():
    with open("tags000000000000.json", "r", encoding="utf-8") as f:
        counter = 1
        data = [json.loads(line) for line in f]
        for line in data:
            if line["category"] == "4":
                name = line["name"]
                post_count = int(line["post_count"])
                Character.objects.create(name=name, post_count=post_count)
                print(f"Processed: {counter}/{len(data)}")
                counter += 1
            else:
                print(f"Processed: {counter}/{len(data)}")
                counter += 1


def parse_posts():
    for root, _, files in os.walk("posts/"):
        files.sort()
        for filename in files:
            file = os.path.join(root, filename)
            with open(file, "r") as f:
                counter = 1
                data = [json.loads(line) for line in f]
                for line in data:
                    if not filter(line):
                        print(f"Processed {counter}/{len(data)} in {filename}")
                        counter += 1
                    else:
                        if waifu_exists(line):
                            update_scores(line)
                            print(f"Processed {counter}/{len(data)} in {filename}")
                            counter += 1
                        else:
                            add_waifu(line)
                            print(f"Processed {counter}/{len(data)} in {filename}")
                            counter += 1


def trim(number: int):
    Waifu.objects.filter(post_count__lt=number).delete()


def attach_post_count():
    waifus = Waifu.objects.all()
    counter = 1
    for waifu in waifus:
        if waifu.post_count == None:
            if Character.objects.filter(name=waifu.name).exists():
                char = Character.objects.get(name=waifu.name)
                waifu.post_count = char.post_count
                waifu.save()
                print(f"Added score: {counter}/{len(waifus)}")
                counter += 1
            else:
                print("Skipped: character not found")
                counter += 1
        else:
            print(f"Skipped: {counter}/{len(waifus)}")
            counter += 1


def attach_rarities():
    waifus = Waifu.objects.all()
    counter = 1
    for waifu in waifus:
        match waifu.post_count:
            case num if num < 100:
                waifu.rarity = "🔯✡✡✡✡"
                waifu.save()
            case num if 100 <= num < 400:
                waifu.rarity = "🔯🔯✡✡✡"
                waifu.save()
            case num if 400 <= num < 2000:
                waifu.rarity = "🔯🔯🔯✡✡"
                waifu.save()
            case num if 2000 <= num < 7500:
                waifu.rarity = "🔯🔯🔯🔯✡"
                waifu.save()
            case num if num >= 7500:
                waifu.rarity = "🔯🔯🔯🔯🔯"
                waifu.save()
            case _:
                pass
        print(f"Processed: {counter}")
        counter += 1


def count_rarities():
    waifus = Waifu.objects.all()
    c = 0
    u = 0
    r = 0
    sr = 0
    ssr = 0
    for waifu in waifus:
        match waifu.rarity:
            case "🔯✡✡✡✡":
                c += 1
            case "🔯🔯✡✡✡":
                u += 1
            case "🔯🔯🔯✡✡":
                r += 1
            case "🔯🔯🔯🔯✡":
                sr += 1
            case "🔯🔯🔯🔯🔯":
                ssr += 1
    print(f"1: {c}\n2: {u}\n3: {r}\n4: {sr}\n5: {ssr}")


def count_by_post_amount(number: int):
    print(len(Waifu.objects.filter(post_count__lt=number)))


def trim_safe():
    Waifu.objects.filter(best_safe_post_score__lt=1).delete()
    Waifu.objects.filter(best_safe_post_score=None).delete()


def trim_unsafe():
    Waifu.objects.filter(best_unsafe_post_score__lt=1).delete()
    Waifu.objects.filter(best_unsafe_post_score=None).delete()


parse_posts()
parse_tags()
attach_post_count()
trim(20)
trim_safe()
trim_unsafe()
attach_rarities()
count_rarities()
