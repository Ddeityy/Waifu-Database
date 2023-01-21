import os
import discord
from discord.ext import commands
from database.model_logic import *
from database.models import *
import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

# client = discord.Client(intents=discord.Intents.all())


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
    message = discord.Embed(
        title=f"{name} (ID:{waifu_obj.id})", description=f"{source}"
    )
    # message.add_field(name="Value", value=f"💎{value}", inline=False)
    message.set_image(url=image)
    message.add_field(
        name="Report",
        value="If this doesn't qualify as waifu,\nPlease send a '$report <ID> <reason>'",
    )

    return message


@bot.command()
async def waifu(ctx, *, id: int =None):
    if id == None:
        waifu = get_random_waifu()
        embed = construct_message(waifu)
        await ctx.reply(embed=embed)
    else try:
            if ctx.author.id == 131503589150556160:
                waifu = get_waifu_by_id(id)
                embed = construct_message(waifu)
                await ctx.reply(embed=embed)
            else:
                pass
        except :
            await ctx.reply("Waifu ID must be an integer.")


@bot.command
@commands.is_owner()
async def delete(ctx, id):
    delete_waifu(id)
    await ctx.reply(f'Deleted "waifu" {id}')


@bot.command()
async def report(ctx, id):
    if isinstance(id, int):
        waifu = get_waifu_by_id(id)
        report(waifu)
        await ctx.reply('"Waifu" reported.')
    else:
        await ctx.reply("Waifu ID must be an integer.")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


bot.run(TOKEN)
