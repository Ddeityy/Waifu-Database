from discord.ext import commands
import dotenv
import discord
from config import config
import os


config()

from db.models import *
from cogs.views import *


dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = commands.Bot(intents=discord.Intents().all())


@bot.event
async def on_connect():
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            bot.load_extension("cogs." + f[:-3])
    print(f"Cogs loaded.")
    await bot.sync_commands()
    print("Commands synced.")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


bot.run(TOKEN)
