from typing import TYPE_CHECKING

from config import MEMBER_COUNT_CHANNEL, MCODING_SERVER
from discord.ext import commands, tasks
from math import log

if TYPE_CHECKING:
    from app.bot import Bot


class MemberCount(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    def get_member_count(self, guild):
        superscript = {
            "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
            "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
            ".": "ˑ"
        }
        mc = guild.member_count
        mc_log = round(log(mc, 2), 3)
        if mc_log % 1 == 0:
            mc_log = int(mc_log)
        mc_log_str = str(mc_log)

        # Comment these 2 out to have 2^8.19 instead of 2⁸ˑ¹⁹
        mc_log_str = f"\b{''.join([superscript[i] for i in mc_log_str])}"

        return f"2^{mc_log_str}"

    @tasks.loop(minutes=10)
    async def update_member_count(self):
        channel = self.bot.get_channel(MEMBER_COUNT_CHANNEL)
        guild = self.bot.get_guild(MCODING_SERVER)
        await channel.edit(name=f"Members: {self.get_member_count(guild)}")

def setup(bot: "Bot"):
    bot.add_cog(MemberCount(bot))
