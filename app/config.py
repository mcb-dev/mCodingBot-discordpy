from typing import Dict, Optional, Type

import dotenv


class Config:

    def __init__(
        self,
        **env: Dict[str, str],
    ):
        def int_or_none(key: str) -> Optional[int]:
            val = env.pop(key, None)

            if val is not None and val.isdigit():
                return int(val)

        self.token = env.pop("TOKEN")

        self.mcoding_server_id = int_or_none("MCODING_SERVER")

        self.member_count_channel_id = int_or_none("MEMBER_COUNT_CHANNEL")

        self.donor_role_id = int_or_none("DONOR_ROLE")
        self.patron_role_id = int_or_none("PATRON_ROLE")

        self.starboard_channel_id = int_or_none("STARBOARD_CHANNEL")
        self.starboard_limit = int_or_none("STARBOARD_LIMIT")

    @classmethod
    def load(cls: Type["Config"], file: str = ".env") -> "Config":
        return cls(**dotenv.dotenv_values(file))
