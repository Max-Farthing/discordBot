import requests
from services.utils import create_game_embed_list, calculate_embed_color
from config import ESPN_BASE_URL, TIMEZONE
from datetime import datetime

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
        embeds = create_game_embed_list(games)

        #header above all embeds
        header = f"🏈 NFL Week {week}: {len(games)} games"

        return header, embeds
    else:
        print(response.text, response.status_code)
        return Exception("API returned failing status: ", response.status_code)

def get_nba_scoreboard():
    """
        Sends GET request to ESPN API to get all current NBA scoreboard information
        for the day

        Returns: Header and a list of Embedded Discord messages to be sent to chat
    """

    response = requests.get(f"{ESPN_BASE_URL}/basketball/nba/scoreboard")

    if response.ok:
        data = response.json()
        games = data.get("events", [])
        month = datetime.now().month
        day = datetime.now().day
        embeds = create_game_embed_list(games)
        embed_header = f"NBA {month}/{day}: {len(games)} games"

        return embed_header, embeds
    else:
        print(response.text, response.status_code)
        return Exception("API returned failing status: ", response.status_code)
