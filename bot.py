import os
import discord
from discord.ext import commands
from django import setup
from discord.ext.commands.errors import NotOwner

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
setup()
from db.models import *
import asyncio
import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

# Waifu commands


@bot.command()
async def capture(ctx, waifu_id: int):
    user_id = ctx.author.id
    if await capture_waifu(waifu_id, user_id):
        await ctx.reply(f"Waifu successfully captured!")
    else:
        await ctx.reply("Waifu already has an owner.")


@bot.command()
async def waifu(ctx):
    waifu = await get_random_waifu()
    owner = await get_waifu_owner(waifu)
    embed = await create_waifu_embed(waifu, owner)
    await ctx.reply(embed=embed)


@bot.command()
# @commands.is_owner()
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
        response = await bot.wait_for("message", timeout=30.0)
    except asyncio.TimeoutError:
        return

    if response.content.lower() == "yes":
        await delete_waifu_db(id)
        await ctx.reply(f'Deleted "waifu" {id}.')
    else:
        return


# User commands
@bot.command()
async def register(ctx):
    user = ctx.author.id
    username = ctx.author
    if await register_user(user, username):
        await ctx.reply(f"Registration complete")
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
async def report(
    ctx,
    waifu_id: int = 0,
    *,
    reason: str = "None",
):
    if id == 0:
        await ctx.reply("Please include waifu ID.")
        return
    if reason == "None":
        await ctx.reply("Please include a reason.")
        return
    user = ctx.author.id
    match await report_waifu(waifu_id, user, reason):
        case "SUCCESS":
            await ctx.reply("Waifu reported.")
        case "DOUBLE":
            await ctx.reply("Waifu already reported.")
        case "DENIED":
            await ctx.reply("Report on this waifu has already been denied.")


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


bot.run(TOKEN)
