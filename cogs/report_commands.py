from config import config
from discord.ext import commands

config()
from db.models import *
from .views import *


class ReportCog(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.is_owner()
    async def reports(self, ctx):
        reports = await get_all_reports()
        if len(reports) > 0:
            for report in reports:
                await ctx.respond(embed=report)
        else:
            await ctx.respond("No reports.")

    @commands.slash_command()
    @commands.is_owner()
    async def accept(self, ctx, id: int):
        if await accept_report(id):
            await ctx.respond("Report accepted!")
        else:
            await ctx.respond("Report not found.")

    @commands.slash_command()
    @commands.is_owner()
    async def accept_all(self, ctx):
        if await accept_all_reports():
            await ctx.respond("All reports accepted.")
        else:
            await ctx.respond("No reports to accept.")

    @commands.slash_command()
    @commands.is_owner()
    async def deny(self, ctx, id: int):
        if await deny_report(id):
            await ctx.respond("Report denied.")
        else:
            await ctx.respond("Report not found.")


def setup(bot):
    bot.add_cog(ReportCog(bot))
