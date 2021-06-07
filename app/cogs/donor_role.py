from typing import TYPE_CHECKING, Optional

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from app.bot import Bot


class DonorRole(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

        self._donor_role: Optional[discord.Role] = None
        self._patron_role: Optional[discord.Role] = None
        self._mcoding_server: Optional[discord.Guild] = None

    @commands.Cog.listener()
    async def on_member_update(
        self, before: discord.Member, after: discord.Member
    ):
        if before.guild.id != self.bot.config.mcoding_server.id:
            return

        if len(before.roles) > len(after.roles):  # they received a role
            return

        added_roles = [r for r in after.roles if r not in before.roles]
        if self.bot.config.patron_role in added_roles:
            await after.add_roles(self.bot.config.donor_role)


def setup(bot: "Bot"):
    bot.add_cog(DonorRole(bot))
