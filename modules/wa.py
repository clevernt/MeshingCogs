import wolframalpha
import os
import asyncio
from twitchio.ext import commands

WOLFRAM_APP_ID = os.environ.get("WA_APP_ID")
wolfram_client = wolframalpha.Client(WOLFRAM_APP_ID)


class WolframAlpha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def query_wolfram(self, query: str) -> str | None:
        try:
            response = await asyncio.to_thread(wolfram_client.query, query)
            answer = response.results.text[500:]
            return answer
        except Exception as e:
            print(e)
            return None

    @commands.command()
    async def wa(self, ctx: commands.Context, *, query: str) -> None:
        answer = await self.query_wolfram(query)
        if answer:
            await ctx.send(f"/me @{ctx.author.name} -> {answer}")
        else:
            await ctx.send(f"/me @{ctx.author.name} -> no answer found you gorilla")


def prepare(bot: commands.Bot):
    bot.add_cog(WolframAlpha(bot))
