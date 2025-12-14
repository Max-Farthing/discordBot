from discord.ext import commands
from services.espn_api import get_nba_scoreboard

class NBA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nbascoreboard(self, ctx):
        try:
            header, embeds = get_nba_scoreboard()

            await ctx.send(header)

            for embed in embeds:
                await ctx.send(embed=embed)
        except:
            await ctx.send("⚠️ Could not fetch NBA scores. Try again later.")

async def setup(bot):
    await bot.add_cog(NBA(bot))
    print("NBA cog loaded ✅")