import os
import discord
from discord.ext import commands
from django import setup
from discord.ext.commands.errors import NotOwner
import asyncio
import dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
setup()
from db.models import *


dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())


# Waifu commands
@bot.command()
async def release(ctx, *, waifu_id: int):
    user = ctx.author.id
    waifu = await get_waifu_by_id(waifu_id)
    name = format_for_embed(waifu.name)
    if waifu.owner_id != None:
        if await release_waifu(waifu.id, user):
            await ctx.reply(f"{name} released.")
        else:
            await ctx.reply(f"You do not own {name}.")
    else:
        await ctx.reply(f"{name} has no owner.")


@bot.command()
async def waifu(ctx):
    waifu = await get_random_waifu()
    owner = await get_waifu_owner(waifu)
    embed = await create_waifu_embed(waifu, owner)
    await ctx.reply(embed=embed)
    try:
        response = await bot.wait_for(
            "message", timeout=30.0, check=lambda x: ctx.author.id == x.author.id
        )
    except asyncio.TimeoutError:
        return
    print(response.content)
    if response.content.lower() == "capture":
        await attempt_capture(3, waifu, ctx, response)
    if response.content.lower().split(" ")[0] == "report":
        reason = " ".join(response.content.lower().split(" ")[1:])
        match await report_waifu(waifu.id, ctx.author.id, reason):
            case "SUCCESS":
                await ctx.reply("Waifu reported.")
            case "DOUBLE":
                await ctx.reply("Waifu is already reported.")
            case "DENIED":
                await ctx.reply("Previous report alredy denied.")
    else:
        return


@bot.command()
@commands.is_owner()
async def waifuid(ctx, id: int):
    waifu = await get_waifu_by_id(id)
    owner = await get_waifu_owner(waifu)
    embed = await create_waifu_embed(waifu, owner)
    await ctx.reply(embed=embed)


@bot.command()
@commands.is_owner()
async def delete_waifu(ctx, id: int):
    await ctx.reply(f"Confirm?")
    try:
        response = await bot.wait_for(
            "message", timeout=30.0, check=lambda x: ctx.author.id == x.author.id
        )
    except asyncio.TimeoutError:
        return

    if response.content.lower() == "yes":
        await delete_waifu_db(id)
        await ctx.reply(f'Deleted "waifu" {id}.')
    else:
        return


# User commands
@bot.command()
async def harem(ctx):
    id = ctx.author.id
    if await check_harem(id):
        waifus = await get_harem(id)
        for waifu in waifus:
            await ctx.reply(embed=waifu)
    else:
        await ctx.reply("No bitches?")


@bot.command()
async def reset(ctx):
    id = ctx.author.id
    name = ctx.author
    await ctx.reply("Are you sure?")
    try:
        response = await bot.wait_for(
            "message", timeout=30.0, check=lambda x: ctx.author.id == x.author.id
        )
    except asyncio.TimeoutError:
        return

    if response.content.lower() == "yes" and response.author == ctx.author:
        if await reset_user(id, name):
            await ctx.reply("User succesfully reset.")
        else:
            await ctx.reply("User not found.")
    else:
        return


@bot.command()
async def register(ctx):
    user = ctx.author.id
    username = ctx.author
    if await register_user(user, username):
        await ctx.reply(f"Registration complete.")
    else:
        await ctx.reply(f"You're already registered.")


@bot.command()
@commands.is_owner()
async def delete_user(ctx, id: int):
    try:
        await delete_user_db(id)
        await ctx.reply(f"User successfully deleted.")
    except NotOwner:
        await ctx.reply(f"No :)")


# Report commands
@bot.command()
@commands.is_owner()
async def reports(ctx):
    try:
        reports = await get_all_reports()
        if len(reports) > 0:
            for report in reports:
                await ctx.reply(embed=report)
        else:
            await ctx.reply("No reports.")
    except NotOwner:
        await ctx.reply("No :)")


@bot.command()
@commands.is_owner()
async def accept(ctx, id: int):
    if await accept_report(id):
        await ctx.reply("Report accepted!")
    else:
        await ctx.reply("Report not found.")


@bot.command()
@commands.is_owner()
async def accept_all(ctx):
    if await accept_all_reports():
        await ctx.reply("All reports accepted.")
    else:
        await ctx.reply("No reports to accept.")


@bot.command()
@commands.is_owner()
async def deny(ctx, id: int):
    if await deny_report(id):
        await ctx.reply("Report denied.")
    else:
        await ctx.reply("Report not found.")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


async def attempt_capture(tries, waifu, ctx, response):
    if tries > 0:
        if await roll(waifu.rarity):
            if await capture_waifu(waifu.id, ctx.author.id):
                name = format_for_embed(waifu.name)
                await ctx.reply(f"Captured {name}.")
            else:
                await ctx.reply(f"{name} already has an owner")
        else:
            tries -= 1
            if tries == 0:
                await ctx.reply("Capture failed.\nGood luck next time!")
                return
            await ctx.reply(f"Capture failed.\nAttempts left: {tries}")
            try:
                new_response = await bot.wait_for(
                    "message",
                    timeout=30.0,
                    check=lambda x: ctx.author.id == x.author.id,
                )
                if new_response.content:
                    await attempt_capture(tries, waifu, ctx, response)
            except asyncio.TimeoutError:
                pass
    else:
        return


bot.run(TOKEN)
