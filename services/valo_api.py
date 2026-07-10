import requests
from config import HENRIK_BASE_URL, VALORANT_API_KEY
import discord
import math
from datetime import datetime, timezone, timedelta

EST = timezone(timedelta(hours=-5), "EST")

def get_recent_game_stats(name, tag, games=1):
    url = f"{HENRIK_BASE_URL}/v1/stored-matches/na/{name}/{tag}?size={games}&mode=competitive"
    headers = {
        "User-Agent": "ValorantTestBot/1.0.0",
        "Authorization": VALORANT_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        body = response.json()

        recent_matches = body.get("data", [])
        embeds = []
        total_combat_score = 0
        wins = 0
        losses = 0
        headshot_percent = 0
        kills = 0
        deaths = 0
        round_count = 0

        for recent_match in recent_matches:

            metaData = recent_match.get("meta")
            mapName = metaData.get("map").get("name")
            gameTime = metaData.get("started_at")
            dt = datetime.fromisoformat(gameTime.replace("Z", "+00:00")).astimezone(EST)
            formatted_date = dt.strftime("%m/%d/%Y %I:%M %p %Z").lower()
            formatted_date = formatted_date.lstrip("0").replace(" 0", " ")
            
            title = mapName
            stats = recent_match.get("stats")

            agent = stats.get("character").get("name")       

            teams = recent_match.get("teams")
            teamColor = stats.get("team").lower()
            result = ''

            team_score = teams.get(teamColor)
            opponent_color = "blue" if teamColor == "red" else "red"
            opponent_score = teams.get(opponent_color)

            if team_score > opponent_score:
                result = "Won"
            elif team_score < opponent_score:
                result = "Lost"
            else:
                result = "Tied"

            embedColor = discord.Colour.from_str("#2ECC71") if result == "Won" else discord.Colour.from_str("#C0392B")
            if result == "Won":
                wins += 1
            else:
                losses += 1

            title += " " + result + ': ' + formatted_date

            embed = discord.Embed(
                title=title,
                color=embedColor
            )

            score = stats.get("score")
            total_combat_score += score
            rounds = team_score + opponent_score
            round_count += rounds
            acs = round(score / rounds)
            
            shots = stats.get("shots")
            headshots = shots.get("head")
            bodyshots = shots.get("body")
            legshots = shots.get("leg")
            total_shots = headshots + bodyshots + legshots
            hs_percent = math.floor(headshots / total_shots * 100) if total_shots else 0
            headshot_percent += hs_percent

            kills += stats.get("kills")
            deaths += stats.get("deaths")

            embed.add_field(name="Player", value=name, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name="Agent", value=agent, inline=True)

            embed.add_field(name="ACS", value=acs, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name="HS%", value=hs_percent, inline=True)

            embed.add_field(name="K", value=stats.get("kills"), inline=True)
            embed.add_field(name="D", value=stats.get("deaths"), inline=True)
            embed.add_field(name="A", value=stats.get("assists"), inline=True)
            embeds.append(embed)
        summary = ""
        total_games = len(recent_matches)
        if total_games > 1:
            total_combat_score /= round_count
            headshot_percent /= total_games
            kills /= deaths

            summary = (
                f"{total_games} Game Averages: "
                f"{total_combat_score:.2f} ACS "
                f"{kills:.2f} K/D "
                f"{headshot_percent:.1f} HS%"
            )
        return summary, embeds
    else: 
        print(response.text, response.status_code)
        raise Exception("API returned failing status: ", response.status_code)
