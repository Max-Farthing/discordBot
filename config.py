import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
VALORANT_API_KEY = os.getenv("VALO_API_KEY")
HENRIK_BASE_URL = "https://api.henrikdev.xyz/valorant"
ESPN_BASE_URL = "https://site.api.espn.com/apis/site/v2/sports"

TIMEZONE = "America/New_York"
