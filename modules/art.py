import twitchio

from typing import Optional

from twitchio.ext import commands
from utils.tweet import get_tweet_id
from utils.art import get_mentions
from utils.sql import Database


class Art(commands.Cog):
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
            return

        # TODO
        # if mentions := get_mentions(message=message.content):
        # if askers := self.database.does_anyone_care(mentions):
        # await message.channel.send(self.database.ping_message(mentions, askers))

    @commands.command(
        aliases=[
            "removecharacter",
            "deletecharacter",
            "removecharacters",
            "deletecharacters",
        ]
    )
    async def remove_character(self, ctx: commands.Context, *, characters: str) -> None:
        success = self.database.remove_characters(
            user_id=ctx.author.id, new_characters=characters
        )

    @commands.command(aliases=["addcharacter", "addcharacters"])
    async def add_character(self, ctx: commands.Context, *, characters: str) -> None:
        self.database.add_characters(user_id=ctx.author.id, new_characters=characters)

    @commands.command(name="characters")
    async def get_characters(
        self, ctx: commands.Context, user: Optional[twitchio.PartialChatter] = None
    ) -> None:
        if user is None:
            user = ctx.author
        characters = self.database.get_characters(user_id=user.id)
        if characters:
            await ctx.send(f"/me {", ".join(characters)}")
        else:
            await ctx.send("/me You do not have any characters")


def prepare(bot: commands.Bot):
    bot.add_cog(Art(bot))
