import requests

from twitchio.ext import commands

games_dict = {
    "genshin": "genshin",
    "hsr": "hkrpg"
}

class Codes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def codes(self, ctx: commands.Context, game: str) -> None:
        if game is None:
            await ctx.send(
                f"/me @{ctx.author.name} -> Please specify a game (Genshin or HSR)"
            )
            return

        if game.lower() not in ["genshin", "hsr"]:
            await ctx.send(
                f"/me @{ctx.author.name} -> Please specify a valid game (Genshin or HSR)"
            )
            return

        resp = requests.get(f"https://hoyo-codes.seriaati.xyz/codes?game={games_dict.get(game.lower()}")
        resp.raise_for_status()
        data = resp.json()
        await ctx.reply(
            f"/me @{ctx.author.name} -> All valid {game} codes {', '.join([code for code in data.get('codes')])}"
        )

def prepare(bot: commands.Bot):
    bot.add_cog(Codes(bot))
