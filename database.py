import sqlite3
from pathlib import Path

DB_PATH = Path("data/bot.db")

def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                discord_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS tracked_players (
                puuid INTEGER PRIMARY KEY,
                discord_id INTEGER,
                player_name TEXT NOT NULL,
                last_match_id TEXT,
                FOREIGN KEY (discord_id) REFERENCES users(discord_id)
            )
        """)             
            