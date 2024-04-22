import twitchio

from twitchio.ext import commands
from utils.tweet import get_tweet_id
from utils.sql import Database


class Repost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    @commands.Cog.event()
    async def event_message(self, message: twitchio.Message):
        if (message.echo) or (message.author.name == "streamelements"):
            return

        tweet_id = get_tweet_id(message=message.content)

        if not tweet_id:
            return

        if self.database.check_repost(tweet_id=tweet_id):
            self.database.add_points(user_id=message.author.id, amount=1)
            await message.channel.send("/me that's a repost")
        else:
            self.database.add_tweet_to_db(tweet_id=tweet_id)


def prepare(bot: commands.Bot):
    bot.add_cog(Repost(bot))
