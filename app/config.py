from typing import Dict, Optional, Type, TYPE_CHECKING, Union
import discord

import dotenv

if TYPE_CHECKING:
    from app.bot import Bot


class Config:
    def __init__(
        self,
        bot: "Bot",
        **env: Dict[str, str],
    ):
        self.bot = bot

        def intornone(key: str) -> Union[int, None]:
            try:
                return int(env.pop(key, None))
            except TypeError:
                return None

        self.token = env.pop("TOKEN")
        self.log_format = env.pop("LOG_FORMAT")

        self.mcoding_server_id = intornone("MCODING_SERVER")
        self.member_count_channel_id = intornone("MEMBER_COUNT_CHANNEL")
        self.donor_role_id = intornone("DONOR_ROLE")
        self.patron_role_id = intornone("PATRON_ROLE")

    @property
    def mcoding_server(self) -> Optional[discord.Guild]:
        try:
            return self._mcoding_server
        except AttributeError:
            self._mcoding_server = self.bot.get_guild(self.mcoding_server_id)
            return self._mcoding_server

    @property
    def member_count_channel(self) -> Optional[discord.VoiceChannel]:
        try:
            return self._member_count_channel
        except AttributeError:
            self._member_count_channel = self.mcoding_server.get_channel(
                self.member_count_channel_id
            )
            return self._member_count_channel

    @property
    def donor_role(self) -> Optional[discord.Role]:
        try:
            return self._donor_role
        except AttributeError:
            self._donor_role = self.mcoding_server.get_role(self.donor_role_id)
            return self._donor_role

    @property
    def patron_role(self) -> Optional[discord.Role]:
        try:
            return self._patron_role
        except AttributeError:
            self._patron_role = self.mcoding_server.get_role(
                self.patron_role_id
            )
            return self._patron_role

    @classmethod
    def load(cls: Type["Config"], bot: "Bot", file: str = ".env") -> "Config":
        return cls(bot, **dotenv.dotenv_values(file))
