from config import config
from discord.ext import commands

config()
from db.models import *
from .views import *


class UserCog(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def harem(self, ctx):
        id = ctx.author.id
        if await check_harem(id):
            waifus = await get_harem(id)
            for waifu in waifus:
                await ctx.respond(embed=waifu)
        else:
            await ctx.respond("https://media.discordapp.net/attachments/1066292810917089370/1069701070890213407/image.png")

    @commands.slash_command()
    async def reset(self, ctx):
        user = ctx.author
        view = ResetView(user)
        await ctx.respond("Are you sure?", view=view)

    @commands.slash_command()
    @commands.is_owner()
    async def nuke_all(self, ctx):
        await nuke_all_users()

    @commands.slash_command()
    @commands.is_owner()
    async def delete_user(self, ctx, id: str):
        await delete_user_db(int(id))
        await ctx.respond(f"User successfully deleted.")


def setup(bot):
    bot.add_cog(UserCog(bot))
