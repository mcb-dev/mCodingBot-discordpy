from typing import Optional, TYPE_CHECKING

import discord
from discord.ext import commands

from config import MCODING_SERVER, DONOR_ROLE, PATRON_ROLE

if TYPE_CHECKING:
    from app.bot import Bot


class DonorRole(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

        self._donor_role: Optional[discord.Role] = None
        self._patron_role: Optional[discord.Role] = None
        self._mcoding_server: Optional[discord.Guild] = None

    @property
    def mcoding_server(self):
        if self._mcoding_server is None:
            self._mcoding_server = self.bot.get_guild(MCODING_SERVER)
        return self._mcoding_server

    @property
    def donor_role(self):
        if self._donor_role is None:
            self._donor_role = self.mcoding_server.get_role(DONOR_ROLE)
        return self._donor_role

    @property
    def patron_role(self):
        if self._patron_role is None:
            self._patron_role = self.mcoding_server.get_role(PATRON_ROLE)
        return self._patron_role

    @commands.Cog.listener()
    async def on_member_update(
        self, before: discord.Member, after: discord.Member
    ):
        if before.guild.id != MCODING_SERVER:
            return

        if len(before.roles) > len(after.roles):  # they received a role
            return

        added_roles = [r for r in after.roles if r not in before.roles]
        if self.patron_role in added_roles:
            await after.add_roles(self.donor_role)


def setup(bot: "Bot"):
    bot.add_cog(DonorRole(bot))
