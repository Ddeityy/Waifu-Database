from config import config
from discord.ext import commands

config()
from db.models import *
from .views import *


class WaifuCog(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def waifu(self, ctx):
        waifu = await get_random_waifu()
        owner = await get_waifu_owner(waifu)
        embed = await create_waifu_embed(waifu, owner)
        capture_button = CaptureView(3, waifu, ctx.author)
        print(ctx.author.id)
        if await register_user(ctx.author.id, ctx.author):
            await ctx.respond(embed=embed, view=capture_button)
        else:
            await ctx.respond(embed=embed, view=capture_button)

    #@commands.slash_command(description="Releases a captured waifu by waifu ID.")
    
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
