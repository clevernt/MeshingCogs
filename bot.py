import os

from datetime import datetime, timezone
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

    @commands.command(name="sethoswhen")
    async def sethoswhen(self, ctx: commands.Context) -> None:
        if ctx.channel.name.lower() == "defendium":
            return

        sethos_date = datetime(2024, 6, 5, 6, 0, 0, tzinfo=timezone.utc)
        current_date = datetime.now(timezone.utc)

        time_left = sethos_date - current_date

        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        await ctx.send(
            f"SETHOS IS COMING OUT IN {days} days, {hours} hours, and {minutes} minutes !!!!!!!!!!!!!!!!!!!!!!!!!!"
        )


bot = MyBot(token=TOKEN, prefix="!", initial_channels=["defendium", "botvuen"])

bot.run()
