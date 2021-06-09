from math import log
from typing import TYPE_CHECKING

from discord.ext import commands, tasks

if TYPE_CHECKING:
    from app.bot import Bot


class MemberCount(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        if self.bot.config.member_count_channel_id is not None:
            self.update_member_count.start()

    @staticmethod
    def get_member_count(guild):
        mc = guild.member_count
        mc_log = round(log(mc, 2), 3)
        if mc_log % 1 == 0:
            mc_log = int(mc_log)
        return f"2**{str(mc_log)}"

    @tasks.loop(minutes=10)
    async def update_member_count(self):
        if not self.bot.is_ready():
            await self.bot.wait_until_ready()
        g = self.bot.mcoding_server
        await self.bot.member_count_channel.edit(
            name=(
                f"Members: {self.get_member_count(g)} " f"({g.member_count})"
            )
        )


def setup(bot: "Bot"):
    bot.add_cog(MemberCount(bot))
