import os
from datetime import datetime, timezone as tz
from typing import Literal
from pymongo import MongoClient


class Database:
    def __init__(self):
        self.client = MongoClient(os.environ.get("MONGODB_URI"))
        self.db = self.client["twitchbot2"]
        self.userdata = self.db["userdata"]
        self.tweets = self.db["tweets"]

        if "created_at_1" not in self.tweets.index_information():
            self.tweets.create_index("created_at", expireAfterSeconds=14 * 24 * 60 * 60)

    def create_user_if_no_exist(self, user_id: int, username: str):
        if not self.userdata.find_one({"user_id": int(user_id)}):
            self.userdata.insert_one({"user_id": int(user_id), "username": username})

    # -- Points --
    def get_points(self, user_id: int, username: str) -> int:
        self.create_user_if_no_exist(user_id, username)
        user = self.userdata.find_one({"user_id": user_id})
        return user.get("points", 0)

    def update_points(
        self,
        user_id: int,
        username: str,
        amount: int,
        operation: Literal["add", "remove", "set"],
    ):
        self.create_user_if_no_exist(user_id, username)

        operations = {
            "add": {"$inc": {"points": amount}},
            "remove": {"$inc": {"points": -amount}},
            "set": {"$set": {"points": amount}},
        }

        self.userdata.update_one({"user_id": user_id}, operations[operation])

    def get_leaderboard(self):
        leaderboard = self.userdata.aggregate(
            [
                {"$sort": {"points": -1}},
                {"$limit": 5},
                {"$project": {"_id": 0, "username": 1, "points": 1}},
            ]
        )
        return list(leaderboard)

    # -- Tweets --
    def get_tweet_timestamp(self, tweet_id: int):
        tweet = self.tweets.find_one({"tweet_id": int(tweet_id)})
        return tweet["created_at"]

    def check_repost(self, tweet_id: int):
        return self.tweets.find_one({"tweet_id": int(tweet_id)}) is not None

    def get_original_poster(self, tweet_id: int):
        try:
            return self.tweets.find_one({"tweet_id": int(tweet_id)})["author"]
        except KeyError:
            return None

    def add_tweet(self, tweet_id: int, author_id: int):
        self.tweets.insert_one(
            {
                "tweet_id": int(tweet_id),
                "author": int(author_id),
                "created_at": datetime.now(tz.utc),
            }
        )

    # --  Characters --
    def add_characters(self, characters, user_id, username):
        self.create_user_if_no_exist(user_id, username)
        self.userdata.update_one(
            {"user_id": int(user_id)},
            {"$addToSet": {"characters": {"$each": characters}}},
        )

    def remove_characters(self, characters, user_id, username):
        self.create_user_if_no_exist(user_id, username)
        self.userdata.update_one(
            {"user_id": int(user_id)}, {"$pull": {"characters": {"$in": characters}}}
        )

    def get_characters(self, user_id, username):
        self.create_user_if_no_exist(user_id, username)
        return (
            self.userdata.find_one({"user_id": int(user_id)}).get("characters", [])
            or None
        )

    def find_askers(self, character):
        users = self.userdata.find(
            {"characters": {"$regex": f"^{character}$", "$options": "i"}}
        )
        usernames = [user["username"] for user in users]
        return usernames
