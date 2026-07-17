from discord.ext import commands
from services.valo_api import (
    get_recent_game_stats,
    get_user_recent_games,
    link_user_to_account,
)

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def link_account(self, ctx, *, player: str):
        name, tag, _ = parse_valorant_player(player, default_count=1)

        try:
            link_user_to_account(name, tag, ctx.author)
            await ctx.send("Discord account linked to Valorant Account")
        except Exception as error:
            print(error)
            await ctx.send("Unable to link account")

    @commands.command()
    async def grm(self, ctx, games: int = 1):
        summary, embeds = get_user_recent_games(ctx.author, games)
        if not embeds:
            await ctx.send("Could not find recent competitive matches")
            return

        if summary:
            await ctx.send(summary)

        for embed in embeds:
            await ctx.send(embed=embed)

    @commands.command()
    async def get_recent_match(self, ctx, *, player: str): 
        
        name, tag, gameCount = parse_valorant_player(player, default_count=1)
        
        try: 
            summary, embeds = get_recent_game_stats(name, tag, gameCount)

            if not embeds:
                await ctx.send("Could not find recent competitive matches")
                return
            
            await ctx.send(summary)
            for embed in embeds:
                await ctx.send(embed=embed)

        except Exception as error:
            print(error)
            await ctx.send("Could not fetch recent match")

    @commands.command()
    async def get_recent_matches(self, ctx, *, player: str):

        name, tag, gameCount = parse_valorant_player(player, default_count=1)
        
        try: 
            summary, embeds = get_recent_game_stats(name, tag, gameCount)

            if not embeds:
                await ctx.send("Could not find recent competitive matches")
                return

            await ctx.send(summary)
            for embed in embeds:
                await ctx.send(embed=embed)

        except Exception as error:
            print(error)
            await ctx.send("Could not fetch recent match")

def parse_valorant_player(player: str, default_count: int):
    parts = player.rsplit(" ", 1)

    gameCount = default_count
    if parts[-1].isdigit():
        gameCount = int(parts[-1])
        player = parts[0]

    try:
        name, tag = player.rsplit(" ", 1)
    except ValueError:
        raise commands.BadArgument("Use: name tag optional_count")

    return name, tag, gameCount

async def setup(bot):
    await bot.add_cog(Valorant(bot))
    print("Valorant cog loaded ✅")

