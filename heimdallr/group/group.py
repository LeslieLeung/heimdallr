import logging
from typing import List

from heimdallr.channel.base import Channel
from heimdallr.channel.factory import build_channel
from heimdallr.config.config import get_config_list, get_config_str
from heimdallr.config.definition import *


class Group:
    def __init__(self, name: str) -> None:
        self.name = name
        self.token: str
        self.channels: List[Channel] = []
        self._build_group()

    def _build_group(self) -> None:
        # get enabled channels
        group_name = str.upper(self.name)
        enabled_channels = get_config_list(group_name, SUFFIX_ENABLED_CHANNELS, [])
        logging.info(f"Group: {group_name}, enabled channels: {enabled_channels}")
        self.token = get_config_str(group_name, SUFFIX_TOKEN, "")

        for channel_name in enabled_channels:
            channel = build_channel(channel_name)
            self.channels.append(channel)
