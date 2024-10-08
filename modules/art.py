import twitchio
import re
from datetime import datetime, timezone

from twitchio.ext import commands
from utils.tweet import get_tweet_id, get_tweet_link
from utils.mongo import Database
from typing import Optional


class Art(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    @commands.Cog.event()
    async def event_message(self, message: twitchio.Message):
        if message.echo or message.author.name.lower() == "streamelements":
            return

        mentions = re.findall(r"@(\w+)", message.content)

        if message.tags.get("reply-parent-msg-body"):
            replied_to_message = message.tags["reply-parent-msg-body"].replace(
                "\\s", " "
            )
            tweet_link = get_tweet_link(replied_to_message)
            tweet_id = get_tweet_id(replied_to_message)
        else:
            tweet_link = get_tweet_link(message.content)
            tweet_id = get_tweet_id(message.content)

        if tweet_link and tweet_id:
            timestamp = self.database.get_tweet_timestamp(tweet_id)
            if (
                not timestamp
                or (datetime.now(tz=timezone.utc) - timestamp).total_seconds() <= 10
            ):
                askers = [
                    user
                    for mention in mentions
                    if (users := self.database.find_askers(mention))
                    for user in users
                ]
                mentioned_characters = [
                    mention
                    for mention in mentions
                    if self.database.find_askers(mention)
                ]

                if askers:
                    askers_str = ", ".join(f"@{user}" for user in askers)
                    mentioned_characters_str = ", ".join(mentioned_characters)
                    botvuen = self.bot.get_channel("botvuen")
                    await botvuen.send(
                        f"/me {askers_str} DinkDonk {mentioned_characters_str} art posted!! {tweet_link}"
                    )

    @commands.command(name="addcharacter", aliases=["addcharacters"])
    async def add_characters(self, ctx: commands.Context, *, characters: str) -> None:
        self.database.add_characters(
            characters.replace(",", "").split(), ctx.author.id, ctx.author.name
        )
        await ctx.send(f"/me {ctx.author.name} -> Updated your characters.")

    @commands.command(
        name="removecharacter",
        aliases=["removecharacters", "deletecharacter", "deletecharacters"],
    )
    async def remove_characters(
        self, ctx: commands.Context, *, characters: str
    ) -> None:
        self.database.remove_characters(
            characters.replace(",", "").split(), ctx.author.id, ctx.author.name
        )
        await ctx.send(f"/me {ctx.author.name} -> Updated your characters.")

    @commands.command(name="characters")
    async def get_characters(
        self,
        ctx: commands.Context,
        target_user: Optional[twitchio.PartialChatter] = None,
    ) -> None:
        if target_user:
            user_id = int((await target_user.user()).id)
            username = target_user.name
        else:
            user_id = int(ctx.author.id)
            username = ctx.author.name

        characters = self.database.get_characters(user_id=user_id, username=username)

        if not characters:
            if target_user:
                await ctx.send(
                    f"/me @{ctx.author.name} -> {target_user.name} has no characters added."
                )
            else:
                await ctx.send(
                    f"/me @{ctx.author.name} -> You don't have characters added."
                )
            return

        if target_user:
            await ctx.send(
                f"/me @{ctx.author.name} -> {target_user.name}'s characters: {', '.join(characters)}"
            )
        else:
            await ctx.send(
                f"/me @{ctx.author.name} -> Your characters: {', '.join(characters)}"
            )


def prepare(bot: commands.Bot):
    bot.add_cog(Art(bot))
