import re
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from app.bot import Bot


class AutoMod(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

        self.bad_strings = (
            (
                re.compile(r"sudo\s+rm"),
                (
                    "`sudo rm` can be dangerous, as it will remove "
                    "any file and is irreversible. Use with care."
                ),
            ),
            (
                re.compile(r".+\(?.*\)?.*{.+\|.+&.*}.*;.*"),
                (
                    "This is a dangerous function and can cause your "
                    "computer to freeze. Please don't run it."
                ),
            ),
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return
        content = message.content.replace("\n", " ")
        for bad_reg, resp in self.bad_strings:
            if bad_reg.findall(content):
                await message.reply(resp)


def setup(bot: "Bot"):
    bot.add_cog(AutoMod(bot))
