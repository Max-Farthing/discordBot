from database import get_connection

def get_user(discord_id: int):
    with get_connection() as connection:
        user = connection.execute(
            "SELECT * FROM users WHERE discord_id = ?",
            (discord_id,)
        ).fetchone()

    return dict(user) if user else None

def save_user(discord_id: int, username: str):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO users (discord_id, username)
            VALUES (?, ?)
            ON CONFLICT(discord_id)
            DO UPDATE SET username = excluded.username
            """,
            (discord_id, username)
        )