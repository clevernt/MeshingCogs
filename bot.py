import os

from twitchio.ext import commands
from twitchio.ext.commands.errors import (
    BadArgument,
    CommandNotFound,
    MissingRequiredArgument,
    CommandOnCooldown,
)

TOKEN: str | None = os.getenv(key="TOKEN")
COGS: list[str] = ["points", "repost", "art"]


class MyBot(commands.Bot):
    async def event_ready(self) -> None:
        print(f"LOGGED IN as {self.nick}")

        for cog in COGS:
            self.load_module(name=f"modules.{cog}")

        print("MODULES LOADED: ", COGS)

    async def event_command_error(self, context: commands.Context, error: Exception):
        if isinstance(error, CommandNotFound):
            return
        if isinstance(error, MissingRequiredArgument):
            await context.send(f"/me Error occurred: {error}")
        if isinstance(error, BadArgument):
            await context.send(f"/me Error occurred: {error}")
        if isinstance(error, CommandOnCooldown):
            await context.send(f"/me Command is on cooldown...")


bot = MyBot(token=TOKEN, prefix="!", initial_channels=["clevernt_"])
bot.run()
