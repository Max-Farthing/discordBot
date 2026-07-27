import requests
from config import HENRIK_BASE_URL, VALORANT_API_KEY
import discord
import math
from datetime import datetime, timezone, timedelta
from repositories import users, tracked_players
import sqlite3

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
                f"{wins} Wins - {losses} Losses + "
                f"{total_games} Game Averages: "
                f"{total_combat_score:.2f} ACS "
                f"{kills:.2f} K/D "
                f"{headshot_percent:.1f} HS%"
            )
        return summary, embeds
    else: 
        print(response.text, response.status_code)
        raise Exception("API returned failing status: ", response.status_code)

def link_user_to_account(name, tag, user):
    url = f"{HENRIK_BASE_URL}/v2/account/{name}/{tag}"
    headers = {
        "User-Agent": "ValorantTestBot/1.0.0",
        "Authorization": VALORANT_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        body = response.json()
        valorant_id = body.get("data").get("puuid")

        # begin logic for storing the provided valorant name + tag and puuid to needed tables in DB
        users.save_user(discord_id=user.id, username=user.name)
        tracked_players.save_player(
            puuid=valorant_id,
            discord_id=user.id,
            player_name=f"{name}#{tag}",
            last_match_id=None
        )

    else:
        print(response.text, response.status_code)
        raise Exception("API returned failing status: ", response.status_code)

def get_user_recent_games(user, games=1):
    try:
        existing_player = tracked_players.find_player_by_discord(user.id)
    except sqlite3.Error as error:
        print("Failed to retrieve Discord User %s", user.id)
        return error

    if not existing_player:
        return "No linked Valorant account found", []

    puuid = existing_player.get("puuid")
    url = f"{HENRIK_BASE_URL}/v4/by-puuid/matches/na/pc/{puuid}?size={games}&mode=competitive"
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
            metadata = recent_match.get("metadata", {})
            map_name = metadata.get("map", {}).get("name")
            game_time = metadata.get("started_at")
            dt = datetime.fromisoformat(game_time.replace("Z", "+00:00")).astimezone(EST)
            formatted_date = dt.strftime("%m/%d/%Y %I:%M %p %Z").lower()
            formatted_date = formatted_date.lstrip("0").replace(" 0", " ")

            player = next(
                (
                    match_player
                    for match_player in recent_match.get("players", [])
                    if match_player.get("puuid") == puuid
                ),
                None
            )
            if not player:
                continue

            player_team = next(
                (
                    team
                    for team in recent_match.get("teams", [])
                    if team.get("team_id") == player.get("team_id")
                ),
                None
            )
            opponent_team = next(
                (
                    team
                    for team in recent_match.get("teams", [])
                    if team.get("team_id") != player.get("team_id")
                ),
                None
            )
            if not player_team or not opponent_team:
                continue

            team_score = player_team.get("rounds", {}).get("won", 0)
            opponent_score = opponent_team.get("rounds", {}).get("won", 0)

            if team_score > opponent_score:
                result = "Won"
                wins += 1
            elif team_score < opponent_score:
                result = "Lost"
                losses += 1
            else:
                result = "Tied"

            embed_color = (
                discord.Colour.from_str("#2ECC71")
                if result == "Won"
                else discord.Colour.from_str("#C0392B")
            )
            embed = discord.Embed(
                title=f"{map_name} {result}: {formatted_date}",
                color=embed_color
            )

            stats = player.get("stats", {})
            score = stats.get("score", 0)
            rounds = team_score + opponent_score
            acs = round(score / rounds) if rounds else 0
            total_combat_score += score
            round_count += rounds

            headshots = stats.get("headshots", 0)
            bodyshots = stats.get("bodyshots", 0)
            legshots = stats.get("legshots", 0)
            total_shots = headshots + bodyshots + legshots
            hs_percent = math.floor(headshots / total_shots * 100) if total_shots else 0
            headshot_percent += hs_percent

            kills += stats.get("kills", 0)
            deaths += stats.get("deaths", 0)

            embed.add_field(
                name="Player",
                value=existing_player.get("player_name"),
                inline=True
            )
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(
                name="Agent",
                value=player.get("agent", {}).get("name"),
                inline=True
            )

            embed.add_field(name="ACS", value=acs, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name="HS%", value=hs_percent, inline=True)

            embed.add_field(name="K", value=stats.get("kills", 0), inline=True)
            embed.add_field(name="D", value=stats.get("deaths", 0), inline=True)
            embed.add_field(name="A", value=stats.get("assists", 0), inline=True)
            embeds.append(embed)

        summary = ""
        total_games = len(embeds)
        if total_games > 1:
            average_combat_score = total_combat_score / round_count if round_count else 0
            average_headshot_percent = headshot_percent / total_games
            kill_death_ratio = kills / deaths if deaths else kills

            summary = (
                f"{wins} Wins - {losses} Losses + "
                f"{total_games} Game Averages: "
                f"{average_combat_score:.2f} ACS "
                f"{kill_death_ratio:.2f} K/D "
                f"{average_headshot_percent:.1f} HS%"
            )

        return summary, embeds
    else:
        print(response.text, response.status_code)
        raise Exception("API returned failing status: ", response.status_code)

def get_mmr(name, tag):
    url = f"{HENRIK_BASE_URL}/v3/mmr/na/pc/{name}/{tag}"
    headers = {
        "User-Agent": "ValorantTestBot/1.0.0",
        "Authorization": VALORANT_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json().get("data")
        current = data.get("current")
        current_tier = current.get("tier")

        current_rank = current_tier.get("name")
        rr = current.get("rr")

        return f"{current_rank}: {rr}rr"
    else:
        print(response.text, response.status_code)
        raise Exception("API returned failing status: ", response.status_code)
