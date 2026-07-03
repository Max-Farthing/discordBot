import requests
from config import HENRIK_BASE_URL, VALORANT_API_KEY
import discord
import math
from datetime import datetime

def get_recent_game_stats(name, tag):
    url = f"{HENRIK_BASE_URL}/v4/matches/na/pc/{name}/{tag}"
    headers = {
        "User-Agent": "ValorantTestBot/1.0.0",
        "Authorization": VALORANT_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        body = response.json()
        data = body.get("data", [])

        recent_match = None
        
        for match in data:
            queue_name = match.get("metadata", {}).get("queue", {}).get("name")
            
            if queue_name == 'Competitive':
                recent_match = match
                break

        metaData = recent_match.get("metadata")
        mapName = metaData.get("map").get("name")
        gameTime = metaData.get("started_at")
        dt = datetime.fromisoformat(gameTime.replace("Z", "+00:00"))
        formatted_date = dt.strftime("%m/%d/%Y %I:%M %p").lower()
        formatted_date = formatted_date.lstrip("0").replace(" 0", " ")
        
        title = mapName

        players = recent_match.get("players")
        foundPlayer = {}
        for player in players:
            if player.get("name") == name:
                foundPlayer = player

        agent = foundPlayer.get("agent").get("name")       

        teams = recent_match.get("teams")
        teamColor = foundPlayer.get("team_id")
        result = ''

        # check team color against 0 and see if they match
        if teams[0].get("team_id") == teamColor:
            result = "Won" if teams[0].get("won") == True else "Lost"
        elif teams[1].get("team_id") == teamColor:
            result = "Won" if teams[1].get("won") == True else "Lost"

        embedColor = discord.Colour.from_str("#2ECC71") if result == "Won" else discord.Colour.from_str("#C0392B")

        title += " " + result + ': ' + formatted_date

        embed = discord.Embed(
            title=title,
            color=embedColor
        )

        stats = foundPlayer.get("stats")
        score = stats.get("score")
        rounds = teams[0].get("rounds").get("won") + teams[0].get("rounds").get("lost")
        acs = round(score / rounds)

        headshots = stats.get("headshots")
        bodyshots = stats.get("bodyshots")
        legshots = stats.get("legshots")
        total_shots = headshots + bodyshots + legshots
        hs_percent = math.floor(headshots / total_shots * 100)

        embed.add_field(name="Player", value=foundPlayer.get("name"), inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True) # Invisible spacer        embed.add_field(name="", value=foundPlayer.get("name"), inline=False)
        embed.add_field(name="Agent", value=agent, inline=True)

        embed.add_field(name="ACS", value=acs, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True) # Invisible spacer        embed.add_field(name="", value=foundPlayer.get("name"), inline=False)
        embed.add_field(name="HS%", value=hs_percent, inline=True)

        embed.add_field(name="K", value=stats.get("kills"), inline=True)
        embed.add_field(name="D", value=stats.get("deaths"), inline=True)
        embed.add_field(name="A", value=stats.get("assists"), inline=True)
        
        return embed
    else: 
        print(response.text, response.status_code)
        return Exception("API returned failing status: ", response.status_code)
