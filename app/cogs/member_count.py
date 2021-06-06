from typing import TYPE_CHECKING

from discord.ext import commands
from math import log

if TYPE_CHECKING:
    from app.bot import Bot


class MemberCount(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    def get_member_count(self, member):
        superscript = {
            "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
            "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
            ".": "ˑ"
        }
        mc = member.guild.member_count
        mc_log = round(log(mc, 2), 3)
        if mc_log % 1 == 0:
            mc_log = int(mc_log)
        mc_log_str = str(mc_log)

        # Comment this out to have 2^8.19 instead of 2⁸ˑ¹⁹
        mc_log_str = "".join([superscript[i] for i in mc_log_str])

        return f"2{mc_log_str}"

    @commands.Cog.listener()
    async def on_member_join(self, member):
        for channel in member.guild.channels:
            if channel.name.startswith("Members: "):
                await channel.edit(name=f"Members: {self.get_member_count(member)}")
                break

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        for channel in member.guild.channels:
            if channel.name.startswith("Members: "):
                await channel.edit(name=f"Members: {self.get_member_count(member)}")
                break


def setup(bot: "Bot"):
    client.add_cog(MemberCount(bot))
