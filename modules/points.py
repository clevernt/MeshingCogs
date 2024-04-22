import twitchio

from typing import Optional

from twitchio.ext import commands
from utils.sql import Database


class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    @commands.command(aliases=["point", "points"])
    async def get_points(
        self, ctx: commands.Context, user: Optional[twitchio.PartialChatter] = None
    ) -> None:
        if user is None:
            user = ctx.author
        points = self.database.get_points(user_id=user.id)
        await ctx.send(f"/me You have {points} points.")

    @commands.command(aliases=["addpoint", "addpoints"])
    async def add_points(self, ctx: commands.Context, user: str, amount: int):
        if not ctx.message.author.is_mod:
            return

        if amount <= 0:
            await ctx.send("/me You must provide an amount")
            return

        if user_object := await self.bot.fetch_users(names=[user]):
            self.database.add_points(user_id=user_object[0].id, amount=amount)
            await ctx.send(f"/me Added {amount} points to {user}")
        else:
            await ctx.send("/me User not found")

    @commands.command(aliases=["removepoints", "deletepoints", "subtractpoints"])
    async def remove_points(self, ctx: commands.Context, user: str, amount: int):
        if not ctx.message.author.is_mod:
            return

        if amount <= 0:
            await ctx.send("/me You must provide an amount")
            return

        if user_object := await self.bot.fetch_users(names=[user]):
            self.database.remove_points(user_id=user_object[0].id, amount=amount)
            await ctx.send(f"/me Subtracted {amount} points from {user}")
        else:
            await ctx.send("/me User not found")

    @commands.command(name="setpoints")
    async def set_points(self, ctx: commands.Context, user: str, amount: int):
        if not ctx.message.author.is_mod:
            return

        if amount < 0:
            await ctx.send("/me Amount must be higher than zero")
            return

        if user_object := await self.bot.fetch_users(names=[user]):
            self.database.set_points(user_id=user_object[0].id, amount=amount)
            await ctx.send(f"/me Set {user}'s points to {amount}")
        else:
            await ctx.send("/me User not found")

    @commands.command(aliases=["lb", "repostlb"])
    async def leaderboard(self, ctx: commands.Context):
        leaderboard = self.database.get_leaderboard()
        usernames = [
            user.name
            for user in await self.bot.fetch_users(
                ids=[user[0] for user in leaderboard]
            )
        ]
        formatted_leaderboard = [
            (username, user[1]) for username, user in zip(usernames, leaderboard)
        ]
        leaderboard_string = ""
        for rank, (username, points) in enumerate(formatted_leaderboard, start=1):
            leaderboard_string += f"{rank}. {username}_{points} points\n"

        await ctx.send(f"/me {leaderboard_string}")


def prepare(bot: commands.Bot):
    bot.add_cog(Points(bot))
