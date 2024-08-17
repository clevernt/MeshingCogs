import twitchio

from typing import Optional
from twitchio.ext import commands
from utils.mongo import Database


class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    @commands.command(name="points")
    async def get_points(
        self, ctx: commands.Context, user: Optional[twitchio.PartialChatter] = None
    ) -> None:
        if user:
            points = self.database.get_points(
                user_id=int((await user.user()).id), username=user.name
            )
            await ctx.reply(
                f"/me @{ctx.author.name} -> {user.name} has {points} points."
            )
        else:
            points = self.database.get_points(
                user_id=int(ctx.author.id), username=ctx.author.name
            )
            await ctx.reply(f"/me @{ctx.author.name} -> You have {points} points.")

    @commands.command(name="addpoints")
    async def add_points(self, ctx: commands.Context, user: twitchio.PartialChatter, amount: int) -> None:
        user_id = int((await user.user()).id)
        self.database.update_points(user_id=user_id, username=user.name, amount=amount, operation="add")
        await ctx.reply(f"/m @{ctx.author.name} -> Added {amount} point(s) to {user.name}")

    @commands.command(name="removepoints")
    async def remove_points(self, ctx: commands.Context, user: twitchio.PartialChatter, amount: int) -> None:
        user_id = int((await user.user()).id)
        self.database.update_points(user_id=user_id, username=user.name, amount=amount, operation="remove")
        await ctx.reply(f"/m @{ctx.author.name} -> Removed {amount} point(s) from {user.name}")

    @commands.command(name="setpoints")
    async def set_points(self, ctx: commands.Context, user: twitchio.PartialChatter, amount: int) -> None:
        user_id = int((await user.user()).id)
        self.database.update_points(user_id=user_id, username=user.name, amount=amount, operation="set")
        await ctx.reply(f"/m @{ctx.author.name} -> Set {user.name}'s points to {amount}")

    @commands.command(aliases=["lb", "repostlb"])
    async def leaderboard(self, ctx: commands.Context):
        lb = self.database.get_leaderboard()
        formatted_lb = [
            f"#{i+1}: {user['username']}_{user['points']}" for i, user in enumerate(lb)
        ]
        await ctx.send(f"/me {', '.join(formatted_lb)}")


def prepare(bot: commands.Bot):
    bot.add_cog(Points(bot))
