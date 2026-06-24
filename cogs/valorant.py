from discord.ext import commands
from services.valo_api import get_recent_game_stats

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get_recent_match(self, ctx, name, tag): 
        try: 
            embed = get_recent_game_stats(name, tag)
            await ctx.send(embed=embed)

        except:
            await ctx.send("Could not fetch recent match")

async def setup(bot):
    await bot.add_cog(Valorant(bot))
    print("Valorant cog loaded ✅")

