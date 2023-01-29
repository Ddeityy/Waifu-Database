import os
from discord.ext import commands
from django import setup


def config():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    setup()
