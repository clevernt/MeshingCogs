import sympy as sp
from twitchio.ext import commands


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def math(self, ctx: commands.Context, expression: str) -> None:
        try:
            result = sp.sympify(expression)
            await ctx.reply(f"/me @{ctx.author.name} -> {result}")
        except Exception as e:
            await ctx.send(f"/me @{ctx.author.name} -> {e}")


def prepare(bot: commands.Bot):
    bot.add_cog(Math(bot))
