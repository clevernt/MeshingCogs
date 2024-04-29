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

    @commands.command(aliases=["lb", "repostlb"])
    async def leaderboard(self, ctx: commands.Context):
        lb = self.database.get_leaderboard()
        formatted_lb = [
            f"#{i+1}: {user['username']}_{user['points']}" for i, user in enumerate(lb)
        ]
        await ctx.reply(f"/me @{ctx.author.name} -> {", ".join(formatted_lb)}")


def prepare(bot: commands.Bot):
    bot.add_cog(Points(bot))
