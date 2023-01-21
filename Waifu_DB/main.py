from django import setup
import json
import os

setup()
from db.models import *

BAD_TAGS = [
    "admiral_(kancolle)",
    "1boy",
    "2boys",
    "3boys",
    "4boys",
    "5boys",
    "6+boys",
    "multiple_girls",
    "multiple_boys",
    "androgynous",
    "body_switch",
    "personality_switch",
    "everyone",
    "multiple_views",
    "guro",
    "scat",
    "pee",
    "baby",
    "tentacles",
    "bestiality",
    "animal_focus",
    "injection",
    "blood",
    "parody",
    "unfinished",
    "sketch",
    "4koma",
    "comic",
    "text_focus",
    "speech_bubble",
    "thought_bubble",
    "animated",
    "animated_gif",
    "animated_png",
    "hybrid_animation",
    "non-repeating_animation",
    "easytoon",
    "looping_animation",
    "flash",
    "ugoira",
    "video",
    "live2d",
    "original",
    "genderswap",
    "cosplay",
]
"""
"tag_string_general":"1boy black_hair chocolate male_focus red_eyes shirt solo striped striped_shirt",
"tag_string":"1boy black_hair chocolate ikari_shinji male_focus neon_genesis_evangelion red_eyes shirt solo striped striped_shirt",
"preview_file_url":"https://cdn.donmai.us/preview/cd/89/cd89a5178b4c827a6e4cf052b7953d61.jpg",
"large_file_url":"https://cdn.donmai.us/original/cd/89/cd89a5178b4c827a6e4cf052b7953d61.png",
"tag_string_character":"ikari_shinji",
"tag_count_copyright":"1",
"is_deleted":true,
"score":"0",
"rating":"s",
"tag_string_copyright":"neon_genesis_evangelion",
"id":"460994",
"tag_count_character":"1",
"""


def update_scores(line):
    waifu_name = line["tag_string_character"].split(" ")[0]
    new_score = line["score"]
    if waifu_name == "":
        return False
    else:
        try:
            waifu = Waifu.objects.get(name=waifu_name)
            current_safe_score = waifu.best_safe_post_score
            current_unsafe_score = waifu.best_unsafe_post_score
            if line["rating"] == "s":
                waifu.best_safe_post_id = int(line["id"])
                waifu.best_safe_post_score = int(line["score"])
                waifu.best_safe_post_image = line["large_file_url"]
                print(current_safe_score)
                if current_safe_score == None:
                    current_safe_score = int(new_score)
                    waifu.save()
                    return True
                else:
                    if current_safe_score <= int(new_score):
                        current_safe_score = int(new_score)
                        waifu.save()
                        return True
                    waifu.save()
                    return True
            else:
                waifu.best_unsafe_post_id = int(line["id"])
                waifu.best_unsafe_post_score = int(line["score"])
                waifu.best_unsafe_post_image = line["large_file_url"]
                if current_unsafe_score == None:
                    current_unsafe_score = int(new_score)
                    waifu.save()
                    return True
                else:
                    if current_unsafe_score <= int(new_score):
                        current_unsafe_score = int(new_score)
                        waifu.save()
                        return True
                    waifu.save()
                    return True
        except KeyError or AttributeError or ValueError:
            pass


def filter(line):
    tags = line["tag_string"].split(" ")
    source_count = int(line["tag_count_copyright"])
    character_count = int(line["tag_count_character"])
    if character_count > 0:
        name = line["tag_string_character"].split(" ")[0]
        if source_count > 0:
            for tag in tags:
                if tag in BAD_TAGS:
                    print("Skipped: bad tags")
                    return False
                if ("solo" or "solo_focus") and "1girl" in tags:
                    if r"_(cosplay)" in name:
                        print("Skipped: cosplay")
                        return False
                    return True
                else:
                    return False
        else:
            print("Skipped: no source")
            return False
    else:
        print("Skipped: no characters")
        return False


files = "posts/"


def add_waifu(line):
    try:
        name = line["tag_string_character"].split(" ")[0]
        if name:
            sources = line["tag_string_copyright"]
            if Waifu.objects.filter(name=name).exists():
                pass
            else:
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


def parse_posts(directory):
    for root, dirs, files in os.walk(directory):
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
                        if Waifu.objects.filter(
                            name=line["tag_string_character"].split(" ")[0]
                        ).exists():
                            update_scores(line)
                            print(f"Processed {counter}/{len(data)} in {filename}")
                            counter += 1
                        else:
                            add_waifu(line)
                            print(f"Processed {counter}/{len(data)} in {filename}")
                            counter += 1


parse_posts(files)
