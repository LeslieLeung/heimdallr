import logging
import os
from typing import List

from environs import Env

logger = logging.getLogger(__name__)

env = Env()
env.read_env(recurse=False)


def get_config_str(name: str, suffix: str, default: str = "") -> str:
    if suffix == "":
        return env.str(name, default)
    return env.str(name + "_" + suffix, default)


def get_config_list(name: str, suffix: str, default: List[str] = []) -> List[str]:
    if suffix == "":
        return env.list(name, default)
    return env.list(name + "_" + suffix, default)


def get_config_int(name: str, suffix: str, default: int = 0) -> int:
    if suffix == "":
        return env.int(name, default)
    return env.int(name + "_" + suffix, default)


def log_env_vars():
    for key, value in os.environ.items():
        logger.debug(f"{key}: {value}")


def is_debug():
    return env.bool("DEBUG", False)
