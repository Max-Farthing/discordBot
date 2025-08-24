import discord
from discord.ext import commands
from services.espn_api import get_nfl_scoreboard

class NFL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nflscoreboard(self, ctx):
        await ctx.send(get_nfl_scoreboard())

async def setup(bot):
    await bot.add_cog(NFL(bot))
    print("NFL cog loaded ✅")

