from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from datetime import datetime

if TYPE_CHECKING:
    from app.bot import Bot


class GhostPingDetection(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        author: discord.Member = message.author

        if author.bot or not message.guild:
            return

        embed = self.bot.embed()
        embed.title = "Ghost Ping Detected !"
        embed.set_author(
            name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
        embed.add_field(name="Message", value=message.content)
        embed.timestamp = str(datetime.utcnow())

        await message.channel.send(embed=embed)


def setup(bot: "Bot"):
    bot.add_cog(GhostPingDetection(bot))
