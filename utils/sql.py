import os
import psycopg2
import logging

from typing import LiteralString

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    name = os.getenv("MYSQLDATABASE")
    host = os.getenv("MYSQLHOST")
    port = int(os.getenv("MYSQLPORT"))
    user = os.getenv("MYSQLUSER")
    password = os.getenv("MYSQLPASSWORD")

    def __init__(self):
        self.name = os.getenv("MYSQLDATABASE")
        self.database = self.create_connection()

    def create_connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.name,
        )

    def get_cursor(self):
        return self.database.cursor()

    # -- Points --
    def get_points(self, user_id: int) -> int:
        cursor = self.get_cursor()
        cursor.execute(
            """
            SELECT points FROM users
            WHERE user_id = %s
            """,
            (user_id,),
        )
        row = cursor.fetchone()
        return row[0] if row else None

    def add_points(self, user_id: int, amount: int) -> None:
        self.get_cursor().execute(
            """
            INSERT INTO users (user_id, points)
            VALUES (%s, %s)
            ON CONFLICT (user_id)
            DO UPDATE SET points = users.points + %s;
            """,
            (user_id, amount, amount),
        )
        self.database.commit()

    def remove_points(self, user_id: int, amount: int) -> None:
        self.get_cursor().execute(
            """
            INSERT INTO users (user_id, points)
            VALUES (%s, %s)
            ON CONFLICT (user_id)
            DO UPDATE SET points = users.points - %s;
            """,
            (user_id, amount, amount),
        )
        self.database.commit()

    def set_points(self, user_id: int, amount: int) -> None:
        self.get_cursor().execute(
            """
            INSERT INTO users (user_id, points)
            VALUES (%s, %s)
            ON CONFLICT (user_id)
            DO UPDATE SET points = %s;
            """,
            (user_id, amount, amount),
        )
        self.database.commit()

    def get_leaderboard(self) -> None:
        cursor = self.get_cursor()
        cursor.execute(
            """
            SELECT user_id, points FROM users ORDER BY points DESC
            """
        )
        return cursor.fetchall()

    # -- Links --
    def add_tweet_to_db(self, tweet_id: int) -> None:
        self.get_cursor().execute(
            """
            INSERT INTO links (tweet_id)
            VALUES (%s)
            """,
            (tweet_id,),
        )
        self.database.commit()

    def check_repost(self, tweet_id: int) -> bool:
        cursor = self.get_cursor()
        cursor.execute(
            """
            SELECT tweet_id FROM links
            WHERE tweet_id = %s
            """,
            (tweet_id,),
        )
        return cursor.fetchone() is not None

    # -- Art --
    def any_askers(self, characters: list) -> list:
        characters_str = ", ".join(["%s"] * len(characters))
        cursor = self.get_cursor()
        cursor.execute(
            f"""
            SELECT user_id FROM users WHERE characters && ARRAY[{characters_str}]
            """
        )
        return cursor.fetchall()

    def add_characters(self, user_id: int, new_characters: list | str) -> None:
        if isinstance(new_characters, list):
            new_characters_array: LiteralString = "{" + ",".join(new_characters) + "}"
        else:
            new_characters_array: LiteralString = "{" + new_characters + "}"

        self.get_cursor().execute(
            """
            INSERT INTO users (user_id, characters)
            VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE
            SET characters = users.characters || %s
            """,
            (user_id, new_characters_array, new_characters_array),
        )

        self.database.commit()

    def remove_characters(self, user_id: int, characters_to_remove: list | str) -> None:
        if isinstance(characters_to_remove, list):
            characters_to_remove_str: LiteralString = (
                "{" + ",".join(characters_to_remove) + "}"
            )
        else:
            characters_to_remove_str: LiteralString = "{" + characters_to_remove + "}"

        self.get_cursor().execute(
            """
            UPDATE users
            SET characters = array_remove(users.characters, %s)
            WHERE user_id = %s
            """,
            (characters_to_remove_str, user_id),
        )

        self.database.commit()

    def get_characters(self, user_id: int) -> str | None:
        cursor = self.get_cursor()
        cursor.execute(
            """
            SELECT characters FROM users
            WHERE user_id = %s
            """,
            (user_id,),
        )
        row = cursor.fetchone()
        return row[0] if row else None
