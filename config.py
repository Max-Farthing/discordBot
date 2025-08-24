import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ESPN_BASE_URL = "https://site.api.espn.com/apis/site/v2/sports"
TIMEZONE = "America/New_York"
