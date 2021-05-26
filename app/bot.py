import os
import platform
import time
from datetime import datetime

import discord
from config import MCODING_SERVER
from discord.ext import commands, prettyhelp
from dotenv import load_dotenv

load_dotenv()

INTENTS = discord.Intents(
    guild_messages=True,
    guild_reactions=True,
    guilds=True,
    members=True,
    presences=True,
)


class Bot(commands.Bot):
    def __init__(self):
        print(
            f"\n-> Starting Bot on Python {platform.python_version()}, "
            f"discord.py {discord.__version__}\n"
        )
        self.log_format = r"%d/%b/%Y:%H:%M:%S"
        self.theme = 0x0B7CD3

        super(Bot, self).__init__(
            command_prefix="!",
            intents=INTENTS,
            help_command=prettyhelp.PrettyHelp(
                color=discord.Color(self.theme),
                command_attrs={"hidden": True},
            ),
        )

        for filename in os.listdir(os.path.join("app", "cogs")):
            if filename.endswith("py"):
                self.load_extension(f"app.cogs.{filename[:-3]}")
        self.load_extension("jishaku")

    def embed(self, **kwargs):
        _embed = discord.Embed(**kwargs, color=self.theme)

        return _embed.set_footer(
            text=(
                f"{self.user.name} - {self.command_prefix}help for "
                "more information"
            ),
            icon_url=self.user.avatar_url,
        )

    def run(self):
        print(
            "       _____       _ _            _____     _",
            " _____|     |___ _| |_|___ ___   | __  |___| |_",
            "|     |   --| . | . | |   | . |  | __ -| . |  _|",
            "|_|_|_|_____|___|___|_|_|_|_  |  |_____|___|_|",
            "                          |___|" "",
            sep="\n",
        )
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
