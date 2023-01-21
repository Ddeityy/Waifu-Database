import os
import discord
import random
from database.model_logic import *
from database.models import *
import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

client = discord.Client(intents=discord.Intents.all())


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


def construct_message(waifu_obj: Waifu):
    name = format_for_embed(waifu_obj.name)
    source = format_for_embed(waifu_obj.source.split(" ")[0])
    if waifu_obj.best_safe_post_image == "None":
        image = waifu_obj.best_unsafe_post_image.replace("/preview/", "/original/")
    else:
        image = waifu_obj.best_safe_post_image.replace("/preview/", "/original/")
    message = discord.Embed(title=f"{name}", description=f"{source}")
    # message.add_field(name="Value", value=f"💎{value}", inline=False)
    message.set_image(url=image)
    return message


@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")


@client.event
async def on_message(message):

    if message.author == client.user:
        return
    if message.content == "$waifu":
        waifu = get_random_waifu()
        embed = construct_message(waifu)
        await message.channel.send(embed=embed)


client.run(TOKEN)
