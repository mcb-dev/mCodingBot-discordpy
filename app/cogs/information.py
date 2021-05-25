from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from app.bot import Bot


class Information(commands.Cog):
    """Bot information"""

    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command(
        name="links",
        help="Useful links."
    )
    async def links(self, ctx: commands.Context):
        embed = self.bot.embed(
            title="Useful Links",
            description="<useful links here>",
        )
        await ctx.send(embed=embed)


def setup(bot: "Bot"):
    bot.add_cog(Information(bot))
