import discord
from discord.ext import commands

class Common(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """Simple hello command"""
        await ctx.send(f"Hello {ctx.author.mention}! 👋")

async def setup(bot):
    await bot.add_cog(Common(bot))
    print("Common cog loaded ✅")