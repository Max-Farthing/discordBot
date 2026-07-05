from discord.ext import commands
from services.valo_api import get_recent_game_stats

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get_recent_match(self, ctx, name, tag, gameCount: int = 1): 
        try: 
            embeds = get_recent_game_stats(name, tag, gameCount)

            if not embeds:
                await ctx.send("Could not find recent competitive matches")
                return

            for embed in embeds:
                await ctx.send(embed=embed)

        except Exception as error:
            print(error)
            await ctx.send("Could not fetch recent match")

    @commands.command()
    async def get_recent_matches(self, ctx, name, tag, gameCount: int = 5):
        try: 
            embeds = get_recent_game_stats(name, tag, gameCount)

            if not embeds:
                await ctx.send("Could not find recent competitive matches")
                return

            for embed in embeds:
                await ctx.send(embed=embed)

        except Exception as error:
            print(error)
            await ctx.send("Could not fetch recent match")

async def setup(bot):
    await bot.add_cog(Valorant(bot))
    print("Valorant cog loaded ✅")

