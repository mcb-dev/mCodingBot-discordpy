import os
import platform
import time
from datetime import datetime
from typing import Optional

import discord
from discord.ext import commands, prettyhelp

from app.config import Config

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

        self.config = Config.load()

        for filename in os.listdir(os.path.join("app", "cogs")):
            if filename.endswith("py"):
                self.load_extension(f"app.cogs.{filename[:-3]}")
        self.load_extension("jishaku")

    @property
    def mcoding_server(self) -> Optional[discord.Guild]:
        try:
            return self._mcoding_server
        except AttributeError:
            self._mcoding_server = self.get_guild(
                self.config.mcoding_server_id
            )
            return self._mcoding_server

    @property
    def member_count_channel(self) -> Optional[discord.VoiceChannel]:
        try:
            return self._member_count_channel
        except AttributeError:
            self._member_count_channel = self.mcoding_server.get_channel(
                self.config.member_count_channel_id
            )
            return self._member_count_channel

    @property
    def donor_role(self) -> Optional[discord.Role]:
        try:
            return self._donor_role
        except AttributeError:
            self._donor_role = self.mcoding_server.get_role(
                self.config.donor_role_id
            )
            return self._donor_role

    @property
    def patron_role(self) -> Optional[discord.Role]:
        try:
            return self._patron_role
        except AttributeError:
            self._patron_role = self.mcoding_server.get_role(
                self.config.patron_role_id
            )
            return self._patron_role

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
        return super().run(self.config.token)

    async def on_command_error(self, ctx: commands.Context, error: Exception):
        await ctx.send(str(error))

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if not message.guild:
            return

        if message.guild.id != self.config.mcoding_server_id:
            return

        await self.process_commands(message)

    async def on_connect(self):
        self.log(f"Logged in as {self.user} after {time.perf_counter():,.3f}s")

    async def on_ready(self):
        self.log(f"Ready after {time.perf_counter():,.3f}s")

    def log(self, *args):
        print(f"[{datetime.now().strftime(self.log_format)}]", *args)
