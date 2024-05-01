import requests

from twitchio.ext import commands


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

        input_game = game.lower()
        if input_game not in ["genshin", "hsr"]:
            await ctx.send(
                f"/me @{ctx.author.name} -> Please specify a valid game (Genshin or HSR)"
            )
            return

        if input_game == "hsr":
            game = "hkrpg"

        resp = requests.get(f"https://hoyo-codes.vercel.app/codes?game={game}")
        resp.raise_for_status()
        data = resp.json()
        await ctx.reply(
            f"/me @{ctx.author.name} -> All valid {input_game} codes {', '.join([code for code in data.get('codes')])}"
        )


def prepare(bot: commands.Bot):
    bot.add_cog(Codes(bot))
