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
        self.owner_ids = [int(user_id) for user_id in env["OWNERS"].split(" ")]

        self.member_count_channel_id = int_or_none("MEMBER_COUNT_CHANNEL")
        self.sub_count_channel = int_or_none("SUBSCRIBER_COUNT_CHANNEL")
        self.view_count_channel = int_or_none("VIEW_COUNT_CHANNEL")

        self.donor_role_id = int_or_none("DONOR_ROLE")
        self.patron_role_id = int_or_none("PATRON_ROLE")

        self.starboard_channel_id = int_or_none("STARBOARD_CHANNEL")
        self.starboard_limit = int_or_none("STARBOARD_LIMIT")

        self.yt_api_key = env.pop("YT_API_KEY", None)
        self.mcoding_yt_id = env.pop("MCODING_YT_ID", None)

        self.autopublish_channel_ids = [
            int(c) for c in env.pop("AUTOPUBLISH_CHANNELS").split(" ")
        ]
        self.autopublish_user_ids = [
            int(c) for c in env.pop("AUTOPUBLISH_USERS").split(" ")
        ]

    @classmethod
    def load(cls: Type["Config"], file: str = ".env") -> "Config":
        return cls(**dotenv.dotenv_values(file))
