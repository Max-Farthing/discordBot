import requests
from config import HENRIK_BASE_URL, VALORANT_API_KEY

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
        recent_match = data[0]
        metadata = recent_match.get("metadata").get("map").get("name")
        
        return metadata
    else: 
        print(response.text, response.status_code)
        return Exception("API returned failing status: ", response.status_code)
