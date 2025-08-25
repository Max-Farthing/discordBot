import discord
from discord.ext import commands
from services.espn_api import get_nfl_scoreboard

class NFL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nflscoreboard(self, ctx):
        try:
            header, embeds = get_nfl_scoreboard()

            await ctx.send(header)

            for embed in embeds:
                await ctx.send(embed=embed)
        except:
            await ctx.send("⚠️ Could not fetch NFL scores. Try again later.")

async def setup(bot):
    await bot.add_cog(NFL(bot))
    print("NFL cog loaded ✅")

