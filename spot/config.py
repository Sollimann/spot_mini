from dataclasses import dataclass
from typing import Optional

from yaml import safe_load
from dacite import from_dict


@dataclass
class SpotConfig:
    hostname: str
    username: str
    password: str
    app_token: Optional[str]


@dataclass
class Config:
    spot: SpotConfig


def read_config(filepath: str) -> Config:
    with open(filepath, "r") as file:
        data = safe_load(file)
        return from_dict(data_class=Config, data=data)  # ['config'])


if __name__ == "__main__":
    config: Config = read_config("../config.yaml")
    print(config)
