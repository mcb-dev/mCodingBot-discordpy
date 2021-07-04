from typing import TYPE_CHECKING
import discord

from discord.ext import commands

if TYPE_CHECKING:
    from app.bot import Bot


class AutoPublisher(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if (not message.guild) or message.guild != self.bot.mcoding_server:
            return

        if (
            message.channel.id in self.bot.config.autopublish_channel_ids
            and message.author.id in self.bot.config.autopublish_user_ids
        ):
            await message.publish()


def setup(bot: "Bot"):
    bot.add_cog(AutoPublisher(bot))
