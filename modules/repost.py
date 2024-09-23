from datetime import datetime, timezone
import twitchio

from twitchio.ext import commands
from utils.tweet import get_tweet_id
from utils.mongo import Database


class Repost(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.database = Database()

    @commands.Cog.event()
    async def event_message(self, message: twitchio.Message):
        if (message.echo) or (message.author.name == "streamelements"):
            return

        tweet_id = get_tweet_id(message=message.content)

        if not tweet_id:
            return

        if self.database.check_repost(tweet_id=tweet_id):
            original_poster_id = self.database.get_original_poster(tweet_id)
            original_poster = (
                (await self.bot.fetch_users(ids=[original_poster_id]))[0]
                if original_poster_id is not None
                else None
            )
            self.database.update_points(
                user_id=int(message.author.id),
                username=message.author.name,
                amount=1,
                operation="add",
            )
            points = self.database.get_points(
                int(message.author.id), message.author.name
            )

            timestamp = self.database.get_tweet_timestamp(tweet_id)
            now = datetime.now(tz=timezone.utc)
            diff = now - timestamp

            seconds = diff.total_seconds()
            minutes = seconds // 60
            hours = minutes // 60
            days = hours // 24

            if minutes < 1:
                timestamp = "just now"
            elif minutes < 60:
                timestamp = f"{int(minutes)} minute(s) ago"
            elif hours < 24:
                timestamp = f"{int(hours)} hour(s) ago"
            else:
                timestamp = f"{int(days)} day(s) ago"

            await message.channel.send(
                f"/me {message.author.mention} -> ⚠️🚨 REPOST DETECTED!!! This was posted {timestamp} by_{original_poster.name}. "
                f"You now have {points} points."
            )
        else:
            self.database.add_tweet(
                tweet_id=tweet_id,
                author_id=int(message.author.id),
            )


def prepare(bot: commands.Bot):
    bot.add_cog(Repost(bot))
