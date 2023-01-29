from config import config
from discord.ext import commands

config()
from db.models import *
from .views import *


class WaifuCog(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def waifu(self, ctx):
        waifu = await get_random_waifu()
        owner = await get_waifu_owner(waifu)
        embed = await create_waifu_embed(waifu, owner)
        capture_button = CaptureView(3, waifu, ctx.author)
        if await register_user(ctx.author.id, ctx.author):
            await ctx.respond(embed=embed, view=capture_button)
        else:
            await ctx.respond(embed=embed, view=capture_button)

    @commands.slash_command(description="Releases a captured waifu by waifu ID.")
    async def release(self, ctx, *, waifu_id: int):
        user = ctx.author.id
        waifu = await get_waifu_by_id(waifu_id)
        name = format_for_embed(waifu.name)
        if waifu.owner_id != None:
            if await release_waifu(waifu.id, user):
                await ctx.respond(f"{name} released.")
            else:
                await ctx.respond(f"You do not own {name}.")
        else:
            await ctx.respond(f"{name} has no owner.")

    @commands.slash_command()
    @commands.is_owner()
    async def waifuid(self, ctx, id: int):
        waifu = await get_waifu_by_id(id)
        owner = await get_waifu_owner(waifu)
        embed = await create_waifu_embed(waifu, owner)
        await ctx.respond(embed=embed)

    @commands.slash_command()
    @commands.is_owner()
    async def delete_waifu(self, ctx, id: int):
        if await delete_waifu_db(id):
            await ctx.respond(f'Deleted "waifu" {id}.')
        else:
            return


def setup(bot):
    bot.add_cog(WaifuCog(bot))
