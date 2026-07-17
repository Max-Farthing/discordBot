from typing import Optional
from database import get_connection

def save_player(puuid: int, discord_id: int, player_name: str, last_match_id: Optional[str] = None):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO tracked_players (puuid, discord_id, player_name, last_match_id)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(puuid)
            DO UPDATE SET
                discord_id = excluded.discord_id,
                player_name = excluded.player_name,
                last_match_id = excluded.last_match_id
            """,
            (puuid, discord_id, player_name, last_match_id)
        )

def find_player_by_discord(discord_id: int):
    with get_connection() as connection:
        player = connection.execute(
            """
            SELECT * FROM tracked_players WHERE discord_id = ?
            """,
            (discord_id,)
        ).fetchone()

    return dict(player) if player else None