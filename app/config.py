from typing import Dict, Type, Union

import dotenv


class Config:
    def __init__(
        self,
        **env: Dict[str, str],
    ):
        def intornone(key: str) -> Union[int, None]:
            try:
                return int(env.pop(key, None))
            except TypeError:
                return None

        self.token = env.pop("TOKEN")

        self.mcoding_server_id = intornone("MCODING_SERVER")
        self.member_count_channel_id = intornone("MEMBER_COUNT_CHANNEL")
        self.donor_role_id = intornone("DONOR_ROLE")
        self.patron_role_id = intornone("PATRON_ROLE")

    @classmethod
    def load(cls: Type["Config"], file: str = ".env") -> "Config":
        return cls(**dotenv.dotenv_values(file))
