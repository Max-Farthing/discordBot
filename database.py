import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

DB_PATH = Path("data/bot.db")


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Yield a configured SQLite connection for one unit of work.

    Successful work is committed. If an exception is raised, the transaction
    is rolled back. The connection is always closed when the block exits.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                discord_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS tracked_players (
                puuid TEXT PRIMARY KEY,
                discord_id INTEGER NOT NULL,
                player_name TEXT NOT NULL,
                last_match_id TEXT,
                FOREIGN KEY (discord_id) REFERENCES users(discord_id)
            )
        """)
