from django.db import models
from random import sample
from asgiref.sync import sync_to_async, async_to_sync
from discord import Embed
from random import randint


class User(models.Model):
    name = models.TextField()
    discord_id = models.IntegerField(unique=True)


@sync_to_async
def nuke_all_users():
    users = User.objects.all()
    users.delete()


@sync_to_async
def check_harem(discord_id: int) -> bool:
    if Waifu.objects.filter(owner_id__discord_id=discord_id).exists():
        return True
    else:
        return False


@sync_to_async
def get_harem(discord_id: int) -> list[Embed]:
    waifus = Waifu.objects.filter(owner_id__discord_id=discord_id).order_by(
        "-post_count"
    )
    embeds = {}
    for waifu in waifus:
        name = format_for_embed(waifu.name)
        source = format_for_embed(waifu.source)
        embed = Embed(title=f"{name} (ID: {waifu.id})", description=source)
        embed.add_field(name="Owner:", value=waifu.owner.name)
        embed.add_field(name="Rarity", value=waifu.rarity)
        embed.set_image(url=waifu.best_unsafe_post_image)
        embeds[waifu.id] = embed
    return embeds


async def reset_user(discord_id: int, name: str):
    if await delete_user_db(discord_id):
        await register_user(id=discord_id, name=name)
        return True
    else:
        return False


@sync_to_async
def register_user(id: int, name: str) -> bool:
    if User.objects.filter(discord_id=id).exists():
        return False
    else:
        User.objects.create(discord_id=id, name=name)
        return True


@sync_to_async
def delete_user_db(id: int) -> bool:
    try:
        user = User.objects.get(discord_id=id)
        user.delete()
        return True
    except:
        return False


class Character(models.Model):
    name = models.TextField(unique=True)
    post_count = models.IntegerField()


class Waifu(models.Model):
    name = models.TextField()
    source = models.TextField()
    post_count = models.IntegerField(null=True)
    best_safe_post_id = models.IntegerField(null=True)
    best_safe_post_score = models.IntegerField(null=True)
    best_safe_post_image = models.TextField(null=True)
    best_unsafe_post_id = models.IntegerField(null=True)
    best_unsafe_post_score = models.IntegerField(null=True)
    best_unsafe_post_image = models.TextField(null=True)
    rarity = models.TextField(null=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


@sync_to_async
def release_waifu(waifu_id: int, owner_id: int):
    waifu = Waifu.objects.get(id=waifu_id)
    if waifu.owner == User.objects.get(discord_id=owner_id):
        waifu.owner = None
        waifu.save()
        return True
    else:
        return False


@sync_to_async
def get_waifu_owner(waifu: Waifu) -> Waifu or None:
    if waifu.owner_id != None:
        owner = waifu.owner_id
        return User.objects.get(id=owner)
    else:
        return None


@sync_to_async
def capture_waifu(waifu_id: int, user_discord_id: int) -> bool:
    if Waifu.objects.filter(owner_id__discord_id=user_discord_id, id=waifu_id).exists():
        return False
    else:
        waifu = Waifu.objects.get(id=waifu_id)
        user = User.objects.get(discord_id=user_discord_id)
        waifu.owner = user
        waifu.save()
        return True


@sync_to_async
def get_waifu_by_id(id: int) -> Waifu:
    return Waifu.objects.get(id=id)


@sync_to_async
def get_random_waifu() -> Waifu:
    waifu = sample(list(Waifu.objects.filter(owner_id=None)), 1)
    return Waifu.objects.get(id=waifu[0].id)


@sync_to_async
def delete_waifu_db(id: int) -> bool:
    waifu = Waifu.objects.get(id=id)
    if waifu.delete():
        return True
    else:
        return False


class Report(models.Model):
    waifu = models.ForeignKey(Waifu, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.TextField()


@sync_to_async
def get_all_reports() -> list[Embed]:
    reports = Report.objects.filter(status="ACTIVE")
    embeds = []
    for report in reports:
        embed = Embed(title="Reports:")
        name = format_for_embed(report.waifu.name)
        embed.add_field(name=f"{name}", value=f"ID:{report.id}")
        embed.set_image(url=report.waifu.best_safe_post_image)
        embeds.append(embed)
    return embeds


@sync_to_async
def accept_all_reports() -> bool:
    reports = Report.objects.filter(status="ACTIVE")
    if reports.exists():
        for report in reports:
            del_waifu_proxy(report.waifu.id)
        return True
    else:
        return


@async_to_sync
async def del_waifu_proxy(waifu):
    return await delete_waifu_db(waifu)


@sync_to_async
def accept_report(id: int) -> bool:
    report = Report.objects.get(id=id)
    if del_waifu_proxy(report.waifu.id):
        return True
    else:
        return False


@sync_to_async
def deny_report(id: int) -> bool:
    if Report.objects.filter(id=id).exists():
        report = Report.objects.get(id=id)
        report.status = "DENIED"
        report.save()
        return True
    else:
        return False


@sync_to_async
def report_waifu(waifu: int, user: int) -> str:
    if report := Report.objects.filter(waifu=waifu).exists():
        if report.status == "ACTIVE":
            return "DOUBLE"
        elif report.status == "DENIED":
            return "DENIED"
    else:
        u = User.objects.get(discord_id=user)
        w = Waifu.objects.get(id=waifu)
        Report.objects.create(waifu=w, user=u, status="ACTIVE")
        return "SUCCESS"


# Utils
def format_for_embed(string: str) -> str:
    if (r"_(") in string:
        name = string.split("_(")[0]
        name = name.split("_")
        name = [word.capitalize() for word in name]
        name = " ".join(name)
        return name
    else:
        name = string.split("_")
        name = [word.capitalize() for word in name]
        name = " ".join(name)
        return name


async def roll(rarity: str) -> bool:
    roll = randint(0, 100)
    match rarity:
        case "🔯✡✡✡✡":
            if roll <= 70:
                return True
            else:
                return False
        case "🔯🔯✡✡✡":
            if roll <= 50:
                return True
            else:
                return False
        case "🔯🔯🔯✡✡":
            if roll <= 30:
                return True
            else:
                return False
        case "🔯🔯🔯🔯✡":
            if roll <= 20:
                return True
            else:
                return False
        case "🔯🔯🔯🔯🔯":
            if roll <= 10:
                return True
            else:
                return False


async def create_waifu_embed(waifu: Waifu, owner: User) -> Embed:
    name = format_for_embed(waifu.name)
    source = format_for_embed(waifu.source.split(" ")[0])
    image = waifu.best_safe_post_image
    rarity = waifu.rarity
    message = Embed(title=f"{name} (ID: {waifu.id})", description=f"{source}")
    if owner == None:
        pass
    else:
        message.add_field(name="Owner", value=owner.name)
    if image == None:
        image = waifu.best_unsafe_post_image
    message.add_field(name="Rarity", value=rarity, inline=False)
    message.set_image(url=image)
    message.add_field(
        name="Report",
        value="If this doesn't qualify as a waifu (wrong character, male character etc.)\nPlease press the report button.",
    )

    return message
