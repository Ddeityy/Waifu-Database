from django.db import models
from random import sample
from asgiref.sync import sync_to_async, async_to_sync
from discord import Embed


class User(models.Model):
    discord_id = models.IntegerField(unique=True)
    money = models.IntegerField(default=0)


@sync_to_async
def register_user(id):
    if User.objects.filter(discord_id=id).exists():
        return False
    else:
        User.objects.create(discord_id=id)
        return True


@sync_to_async
def delete_user_db(id):
    user = User.objects.filter(discord_id=id)
    user.delete()


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
    value = models.IntegerField(null=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


@sync_to_async
def get_waifu_by_id(id):
    return Waifu.objects.get(id=id)


@sync_to_async
def get_random_waifu():
    waifu = sample(list(Waifu.objects.all()), 1)
    return waifu[0].id


@sync_to_async
def delete_waifu_db(id):
    waifu = Waifu.objects.get(id=id)
    if waifu.owner != None:
        waifu.owner.money += 500
        waifu.delete()
        return True
    else:
        waifu.delete()
        return True


class Report(models.Model):
    waifu = models.ForeignKey(Waifu, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.TextField()


@sync_to_async
def get_all_reports():
    reports = Report.objects.filter(status="ACTIVE")
    embeds = []
    for report in reports:
        embed = Embed(title="Reports:")
        name = format_for_embed(report.waifu.name)
        embed.add_field(name=f"{name} ID:{report.id}", value=f"{report.reason}")
        embed.set_image(url=report.waifu.best_safe_post_image)
        embeds.append(embed)
    return embeds


@sync_to_async
def accept_all_reports():
    reports = Report.objects.filter(status="ACTIVE")
    for report in reports:
        del_waifu_proxy(report.waifu.id)
    return True


@async_to_sync
async def del_waifu_proxy(waifu):
    return await delete_waifu_db(waifu)


@sync_to_async
def accept_report(id: int):
    report = Report.objects.get(id=id)
    if del_waifu_proxy(report.waifu.id):
        return True


@sync_to_async
def deny_report(id: int):
    report = Report.objects.get(id=id)
    report.status = "DENIED"
    report.save()
    return True


@sync_to_async
def report_waifu(waifu: int, user: int, reason: str):
    if report := Report.objects.filter(waifu=waifu).exists():
        if report.status == "ACTIVE":
            return "DOUBLE"
        elif report.status == "DENIED":
            return "DENIED"
    else:
        u = User.objects.get(discord_id=user)
        w = Waifu.objects.get(id=waifu)
        r = reason
        Report.objects.create(waifu=w, user=u, reason=r, status="ACTIVE")
        return "SUCCESS"


# Utils


def format_for_embed(string):
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


async def construct_message(id: int):
    waifu_obj = await get_waifu_by_id(id)
    name = format_for_embed(waifu_obj.name)
    source = format_for_embed(waifu_obj.source.split(" ")[0])
    image = waifu_obj.best_safe_post_image
    if image == None:
        image = waifu_obj.best_unsafe_post_image
    message = Embed(title=f"{name} (ID: {waifu_obj.id})", description=f"{source}")
    # message.add_field(name="Value", value=f"💎{value}", inline=False)
    message.set_image(url=image)
    message.add_field(
        name="Report",
        value="If this doesn't qualify as waifu,\nPlease send a '$report <ID> <reason>'",
    )

    return message
