import requests
import discord
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from config import ESPN_BASE_URL, TIMEZONE

def get_nfl_scoreboard():
    """
        Sends GET request to ESPN API to get all current NFL scoreboard information
        for the current week

        Returns: Header and a list of Embedded Discord messages to be sent to chat
    """
    response = requests.get(f"{ESPN_BASE_URL}/football/nfl/scoreboard")

    if response.ok:
        data = response.json()
        games = data.get("events", [])
        week = data.get("week")["number"]
        embeds = []

        #header above all embeds
        header = f"🏈 NFL Week {week}: {len(games)} games"

        #loop through all games in week
        for game in games:

            name = game["name"]
            competition = game["competitions"][0]
            state = competition["status"]["type"]["state"]

            #determine what color to make Embed object
            if state == "pre":
                color = discord.Colour.from_str("#95A5A6")
            elif state == "in":
                color = discord.Colour.from_str("#2ECC71")
            else:
                color = discord.Colour.from_str("#C0392B")

            #create Embed object
            embed = discord.Embed(
                title=name,
                color=color,
            )

            #Gameclock or Game details based upon state of game
            time = competition["status"]["type"]["shortDetail"]
            embed.add_field(name="", value=time, inline=False)

            #grab team information
            team1 = competition["competitors"][0]
            team2 = competition["competitors"][1]

            team1_abbr = team1["team"]["abbreviation"]
            team2_abbr = team2["team"]["abbreviation"]

            team1_score = team1["score"]
            team2_score = team2["score"]

            #set teams and scores
            embed.add_field(name=team1_abbr, value=team1_score, inline=True)
            embed.add_field(name=team2_abbr, value=team2_score, inline=True)

            #append embed to list of embeds
            embeds.append(embed)

        return header, embeds
    else:
        return 0
