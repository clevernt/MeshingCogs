import requests
import re

from twitchio.ext import commands

games_dict = {
    "genshin": "genshin",
    "hsr": "hkrpg",
    "zzz": "nap",
}


class Codes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def codes(self, ctx: commands.Context, game: str = None) -> None:
        if game is None:
            await ctx.send(
                f"/me @{ctx.author.name} -> Please specify a game (genshin, hsr, or zzz)"
            )
            return

        if game.lower() not in ["genshin", "hsr", "zzz"]:
            await ctx.send(
                f"/me @{ctx.author.name} -> Please specify a valid game (genshin, hsr, or zzz)"
            )
            return

        resp = requests.get(
            f"https://hoyo-codes.seria.moe/codes?game={games_dict.get(game.lower())}"
        )
        if resp.status_code != 200:
            await ctx.send(f"/me @{ctx.author.name} -> Failed to fetch codes.")
            return

        data = resp.json()
        codes = [
            code["code"]
            for code in data["codes"]
            if re.search(
                r"\b(primogem|primogems|stellar jade|stellar jades|polychrome|polychromes)\b",
                code["rewards"],
                re.IGNORECASE,
            )
        ]

        if not codes:
            await ctx.send(f"/me @{ctx.author.name} -> No codes found for {game}.")
            return

        await ctx.send(
            f"/me @{ctx.author.name} -> All active {game} codes: {" ".join(codes)}"
        )


def prepare(bot: commands.Bot):
    bot.add_cog(Codes(bot))
