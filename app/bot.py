import os
import time
from datetime import datetime

import discord
from discord.ext import commands, prettyhelp
from dotenv import load_dotenv

from config import MCODING_SERVER

load_dotenv()

INTENTS = discord.Intents.default()
INTENTS.members = True


class Bot(commands.Bot):
    def __init__(self):
        self.log_format = r"%d/%b/%Y:%H:%M:%S"
        self.theme = 0x0B7CD3

        super(Bot, self).__init__(
            command_prefix="!",
            intents=INTENTS,
            help_command=prettyhelp.PrettyHelp(
                color=self.theme, show_index=False,
            ),
        )

        for filename in os.listdir(os.path.join("app", "cogs")):
            if filename.endswith('py'):
                self.load_extension(f"app.cogs.{filename[:-3]}")
        self.load_extension("jishaku")

    def embed(self, **kwargs):
        _embed = discord.Embed(**kwargs, color=self.theme)

        return _embed.set_footer(
            text=(
                f"{self.user.name} - {self.command_prefix}help for "
                "more information"
            ),
            icon_url=self.user.avatar_url
        )

    def run(self):
        return super().run(os.getenv("TOKEN"))

    async def on_command_error(self, ctx: commands.Context, error: Exception):
        await ctx.send(str(error))

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if not message.guild:
            return

        if message.guild.id != MCODING_SERVER:
            return

        await self.process_commands(message)

    async def on_connect(self):
        self.log(f"Logged in as {self.user} after {time.perf_counter():,.3f}s")

    async def on_ready(self):
        self.log(f"Ready after {time.perf_counter():,.3f}s")

    def log(self, *args):
        print(f"[{datetime.now().strftime(self.log_format)}]", *args)
