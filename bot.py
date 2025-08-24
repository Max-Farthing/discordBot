import discord
from discord.ext import commands
from dotenv import load_dotenv
from config import DISCORD_TOKEN
import asyncio

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content

bot = commands.Bot(command_prefix='!', intents=intents)

initial_extensions = [
    "cogs.common",
    "cogs.nfl"
]

async def main():
    for ext in initial_extensions:
        await bot.load_extension(ext)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')

    await bot.start(DISCORD_TOKEN)

asyncio.run(main())
