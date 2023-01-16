import os
import discord
import random
import datetime

TOKEN = os.getenv("TOKEN")

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")


@client.event
async def on_message(message):

    global counter
    global lowest_roll

    if message.author == client.user:
        return


client.run(TOKEN)
