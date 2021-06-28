from typing import TYPE_CHECKING

from discord.ext import commands, tasks

if TYPE_CHECKING:
    from app.bot import Bot


class DonorRole(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.check_missing_donor_role.start()

    @tasks.loop(minutes=1)
    async def check_missing_donor_role(self):
        await self.bot.wait_until_ready()
        if not self.bot.mcoding_server.chunked:
            await self.bot.mcoding_server.chunk()

        patron_role = self.bot.patron_role
        for member in patron_role.members:
            if self.bot.donor_role not in member.roles:
                await member.add_roles(self.bot.donor_role)


def setup(bot: "Bot"):
    bot.add_cog(DonorRole(bot))
