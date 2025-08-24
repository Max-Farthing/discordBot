import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta, timezone

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

@bot.command()
async def nflscoreboard(ctx, cutOffDays: int = 3):
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    resp = requests.get(url)

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=cutOffDays)

    if not resp.ok:
        await ctx.send(f"Error fetching data: {resp.status_code}")
        return

    games = resp.json().get("events", [])
    if not games:
        await ctx.send("No NFL games found.")
        return

    NFL_LOGO = "https://a.espncdn.com/i/teamlogos/nfl/500/nfl.png"  # neutral placeholder

    for game in games:
        game_date = datetime.fromisoformat(game["date"].replace("Z", "+00:00"))
        if game_date < cutoff:
            continue

        status = game["status"]["type"]["shortDetail"]
        state = game["status"]["type"]["state"]  # 'pre', 'in', 'post'
        scores = game["competitions"][0]["competitors"]

        team1 = scores[0]["team"]
        team2 = scores[1]["team"]

        score1 = int(scores[0]['score'])
        score2 = int(scores[1]['score'])

        # Determine thumbnail
        if state == "post":  # finished
            if score1 > score2:
                thumbnail = team1["logo"]
                score1_display = f"**{score1} 🏆**"
                score2_display = f"{score2}"
            elif score2 > score1:
                thumbnail = team2["logo"]
                score1_display = f"{score1}"
                score2_display = f"**{score2} 🏆**"
            else:  # tie
                thumbnail = None
                score1_display = f"{score1}"
                score2_display = f"{score2}"
        elif state == "in":  # live
            thumbnail = None
            score1_display = f"{score1}"
            score2_display = f"{score2}"
        else:  # upcoming
            thumbnail = NFL_LOGO
            score1_display = f"{score1}"
            score2_display = f"{score2}"

        # Set embed color
        color = 0x00ff00 if state == "in" else 0x808080 if state == "post" else 0x3498db
        title_prefix = "LIVE 🔴\n" if state == "in" else ""
        embed = discord.Embed(
            title=f"{title_prefix}{game['name']}",
            description=status if state != "pre" else f"Scheduled: {game_date.strftime('%Y-%m-%d %H:%M UTC')}",
            color=color
        )

        embed.add_field(name=team1["abbreviation"], value=score1_display, inline=True)
        embed.add_field(name=team2["abbreviation"], value=score2_display, inline=True)

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        embed.set_footer(text=f"Game date: {game_date.strftime('%Y-%m-%d %H:%M UTC')}")

        await ctx.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))