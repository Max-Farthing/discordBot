import discord
from discord.ext import commands
from services.espn_api import get_nfl_scoreboard

class NFL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nflscoreboard(self, ctx):
        header, embeds = get_nfl_scoreboard()

        await ctx.send(header)

        for embed in embeds:
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NFL(bot))
    print("NFL cog loaded ✅")

