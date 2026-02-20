import os
from dataclasses import dataclass


@dataclass
class TonnelConfig:
    auth_data: str


def load_tonnel_config() -> TonnelConfig:
    return TonnelConfig(
        auth_data=os.environ["TONNEL_AUTH_DATA"]
    )
