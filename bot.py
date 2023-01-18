import os
import discord
import random
from database.model_logic import *
from database.models import *
import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

client = discord.Client(intents=discord.Intents.all())


def construct_message(waifu_obj: Waifu):
    name = waifu_obj.full_name
    if waifu_obj.age == "Unknown":
        age = ""
    else:
        age = f"({waifu_obj.age})"
    title = waifu_obj.source_title
    image = waifu_obj.image_url
    value = waifu_obj.value
    message = discord.Embed(title=f"{name} {age}", description=f"{title}")
    message.add_field(name="Value", value=f"💎{value}", inline=False)
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
        waifu = get_random_waifu(random.randint(1, 6284))
        embed = construct_message(waifu)
        await message.channel.send(embed=embed)


client.run(TOKEN)
