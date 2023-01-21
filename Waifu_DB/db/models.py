from django.db import models
from random import randint


class User(models.Model):
    discord_id = models.IntegerField()
    money = models.IntegerField(default=0)


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


class Report(models.Model):
    waifu = models.ForeignKey(Waifu, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.TextField()


def get_waifu_by_id(id):
    return Waifu.objects.get(id=id)


def get_random_waifu():
    id_range = len(Waifu.objects.all())
    print(id_range)
    id = randint(1, id_range)
    return Waifu.objects.get(id=id)
