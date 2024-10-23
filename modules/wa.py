import wolframalpha
import os
from twitchio.ext import commands

WOLFRAM_APP_ID = os.environ.get("WA_APP_ID")
wolfram_client = wolframalpha.Client(WOLFRAM_APP_ID)


class WolframAlpha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wa(self, ctx: commands.Context, *, query: str) -> None:
        try:
            response = wolfram_client.query(query)
            answer = next(response.results).text
            await ctx.send(f"/me @{ctx.author.name} -> {answer}")
        except Exception as e:
            await ctx.send(f"/me @{ctx.author.name} -> no answer found you gorilla")


def prepare(bot: commands.Bot):
    bot.add_cog(WolframAlpha(bot))
