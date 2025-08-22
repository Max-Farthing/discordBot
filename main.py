import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author}')

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(f"The sum is {a + b}")

bot.run(os.getenv("DISCORD_TOKEN"))