import twitchio

from twitchio.ext import commands
from utils.tweet import get_tweet_id
from utils.mongo import Database


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
            self.database.update_points(
                user_id=int(message.author.id),
                username=message.author.name,
                amount=1,
                operation="add",
            )
            await message.channel.send(
                f"/me {message.author.mention} -> ⚠️🚨 REPOST DETECTED!!! "
                "YOU HAVE BEEN REPORTED TO THE HIGHER-UPS (WHO DON'T EXIST) "
                f"AND YOU NOW HAVE "
                f"{self.database.get_points(int(message.author.id), message.author.name)}"
                " POINTS"
            )
        else:
            self.database.add_tweet(tweet_id=tweet_id)


def prepare(bot: commands.Bot):
    bot.add_cog(Repost(bot))
