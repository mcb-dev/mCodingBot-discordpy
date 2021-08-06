import os
import platform
import time
import random
from datetime import datetime
from typing import Optional

import discord
from aiocache import cached
from discord.ext import commands, prettyhelp

from app.config import Config
from app.database.database import Database

INTENTS = discord.Intents(
    guild_messages=True,
    guild_reactions=True,
    guilds=True,
    members=True,
    presences=True,
)


class Bot(commands.Bot):
    def __init__(self):
        self._mcoding_server: Optional[discord.Guild] = None
        self._member_count_channel: Optional[discord.VoiceChannel] = None
        self._donor_role: Optional[discord.Role] = None
        self._patron_role: Optional[discord.Role] = None
        self._starboard_channel: Optional[discord.TextChannel] = None
        self._sub_count_channel: Optional[discord.VoiceChannel] = None
        self._view_count_channel: Optional[discord.VoiceChannel] = None

        print(
            f"\n-> Starting Bot on Python {platform.python_version()}, "
            f"discord.py {discord.__version__}\n"
        )
        self.log_format = r"%d/%b/%Y:%H:%M:%S"
        self.theme = 0x0B7CD3

        super(Bot, self).__init__(
            command_prefix=commands.when_mentioned_or("m!"),
            intents=INTENTS,
            help_command=prettyhelp.PrettyHelp(
                color=discord.Color(self.theme),
                command_attrs={"hidden": True},
            ),
            allowed_mentions=discord.AllowedMentions.none(),
        )

        self.config = Config.load()
        self.db = Database()

        for filename in os.listdir(os.path.join("app", "cogs")):
            if filename.endswith("py"):
                self.load_extension(f"app.cogs.{filename[:-3]}")

        self.load_extension("jishaku")

    async def is_owner(self, user: discord.User):
        if user.id in self.config.owner_ids:
            return True
        return await super().is_owner(user)

    @property
    def mcoding_server(self) -> Optional[discord.Guild]:
        if self._mcoding_server is None:
            self._mcoding_server = self.get_guild(
                self.config.mcoding_server_id
            )
        return self._mcoding_server

    @property
    def member_count_channel(self) -> Optional[discord.VoiceChannel]:
        if self._member_count_channel is None:
            self._member_count_channel = self.mcoding_server.get_channel(
                self.config.member_count_channel_id
            )

        return self._member_count_channel

    @property
    def view_count_channel(self) -> Optional[discord.VoiceChannel]:
        if self._view_count_channel is None:
            self._view_count_channel = self.mcoding_server.get_channel(
                self.config.view_count_channel
            )

        return self._view_count_channel

    @property
    def sub_count_channel(self) -> Optional[discord.VoiceChannel]:
        if self._sub_count_channel is None:
            self._sub_count_channel = self.mcoding_server.get_channel(
                self.config.sub_count_channel
            )

        return self._sub_count_channel

    @property
    def donor_role(self) -> Optional[discord.Role]:
        if self._donor_role is None:
            self._donor_role = self.mcoding_server.get_role(
                self.config.donor_role_id
            )

        return self._donor_role

    @property
    def patron_role(self) -> Optional[discord.Role]:
        if self._patron_role is None:
            self._patron_role = self.mcoding_server.get_role(
                self.config.patron_role_id
            )

        return self._patron_role

    @property
    def starboard_channel(self) -> Optional[discord.TextChannel]:
        if self._starboard_channel is None:
            self._starboard_channel = self.mcoding_server.get_channel(
                self.config.starboard_channel_id
            )

        return self._starboard_channel

    @cached(ttl=10)
    async def fetch_message(
        self, channel: discord.TextChannel, message_id: int
    ) -> Optional[discord.Message]:
        try:
            return await channel.fetch_message(message_id)

        except discord.NotFound:
            return

    def embed(self, **kwargs):
        _embed = discord.Embed(**kwargs, color=self.theme)

        return _embed.set_footer(
            text=f"{self.user.name} - m!help for " "more information",
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

    async def start(self, *args, **kwargs):
        await self.db.init()
        await super().start(*args, **kwargs)

    async def close(self):
        await self.db.close()
        return await super().close()

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

    async def on_member_join(self, member: discord.Member):
        if member.guild.id != self.config.mcoding_server_id:
            #Safe to return since this bot will not be on servers besides MCoding
            return

        channel_id = self.config.welcome_channel
        if channel_id is None:
            self.log("WELCOME_CHANNEL environment variable is not defined. Member join message will not be sent.")
            return

        channel = self.get_channel(channel_id)
        join_message = random.choice(self.config.join_messages)
        message = await channel.send(join_message.format(member=member.mention))
        await message.add_reaction("👋")

    async def on_connect(self):
        self.log(f"Logged in as {self.user} after {time.perf_counter():,.3f}s")

    async def on_ready(self):
        self.log(f"Ready after {time.perf_counter():,.3f}s")

    def log(self, *args):
        print(f"[{datetime.now().strftime(self.log_format)}]", *args)
