import os
import discord
from discord.ext import commands
from django import setup

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
async def waifu(ctx):
    waifu = await get_random_waifu()
    embed = await construct_message(waifu)
    await ctx.reply(embed=embed)


@bot.command()
@commands.is_owner()
async def waifuid(ctx, id: int):
    waifu = get_waifu_by_id(id)
    embed = await construct_message(waifu)
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
        await ctx.reply(f'Deleted "waifu" {id}')
    else:
        return


# User commands
@bot.command()
async def register(ctx):
    user = ctx.author.id
    if await register_user(user):
        await ctx.reply(f"Registration complete")
    else:
        await ctx.reply(f"You're already registered.")


@bot.command()
@commands.is_owner()
async def delete_user(ctx, id: int):
    await delete_user_db(id)
    await ctx.reply(f"User {ctx.author} successfully deleted")


# Report commands
@bot.command()
@commands.is_owner()
async def reports(ctx):
    reports = await get_all_reports()
    if len(reports) > 0:
        for report in reports:
            await ctx.reply(embed=report)
    else:
        await ctx.reply("No reports.")


@bot.command()
async def report(
    ctx,
    waifu_id: int = 0,
    *,
    reason: str = "None",
):
    if id == 0:
        await ctx.reply("Please include waifu ID.")
    if reason == "None":
        await ctx.reply("Please include a reason.")
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


@bot.command()
@commands.is_owner()
async def accept_all(ctx):
    if await accept_all_reports():
        await ctx.reply("All reports accepted")


@bot.command()
@commands.is_owner()
async def deny(ctx, id: int):
    if await deny_report(id):
        await ctx.reply("Report denied")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


bot.run(TOKEN)
