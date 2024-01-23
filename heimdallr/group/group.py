import logging
from typing import List

from heimdallr.channel.base import Channel
from heimdallr.channel.factory import build_channel
from heimdallr.config.config import get_config_list, get_config_str
from heimdallr.config.definition import SUFFIX_ENABLED_CHANNELS, SUFFIX_TOKEN


class Group:
    def __init__(self, name: str) -> None:
        self.name = name
        self.token: str = get_config_str(self.name, SUFFIX_TOKEN, "")
        self.channels: List[Channel] = []
        self._is_initialized: bool = False

    def _build_group(self) -> None:
        # get enabled channels
        enabled_channels = get_config_list(self.name, SUFFIX_ENABLED_CHANNELS, [])
        logging.info(f"Group: {self.name}, enabled channels: {enabled_channels}")

        for channel_name in enabled_channels:
            channel = build_channel(channel_name)
            self.channels.append(channel)

        self._is_initialized = True

    def activate(self) -> None:
        if not self._is_initialized:
            self._build_group()
