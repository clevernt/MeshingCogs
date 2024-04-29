import os

from twitchio.ext import commands
from twitchio.ext.commands.errors import (
    BadArgument,
    CommandNotFound,
    MissingRequiredArgument,
)

TOKEN: str = os.getenv(key="TOKEN")
COGS = ["points", "repost", "art", "codes"]


class MyBot(commands.Bot):
    async def event_ready(self) -> None:
        print(f"LOGGED IN as {self.nick}")

        for cog in COGS:
            self.load_module(name=f"modules.{cog}")

        print("MODULES LOADED: ", COGS)

    async def event_command_error(self, context: commands.Context, error: Exception):
        if isinstance(error, CommandNotFound):
            return
        elif isinstance(error, MissingRequiredArgument):
            await context.send(f"/me {error}")
        elif isinstance(error, BadArgument):
            await context.send(f"/me {error}")
        else:
            print(error)


bot = MyBot(
    token=TOKEN, prefix="!", initial_channels=["defendium", "botvuen", "clevernt_"]
)

bot.run()
