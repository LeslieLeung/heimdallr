import logging
from typing import List

from heimdallr.channel.base import Channel
from heimdallr.channel.factory import build_channel
from heimdallr.config.config import get_config_list, get_config_str, has_key
from heimdallr.config.definition import (
    SUFFIX_ENABLED_CHANNELS,
    SUFFIX_TOKEN,
    SUFFIX_TYPE,
)


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

        for name in enabled_channels:
            # it could be a channel or a group
            if has_key(name, SUFFIX_TYPE):
                # channel
                channel = build_channel(name)
                self.channels.append(channel)
            else:
                # group
                if name == self.name:
                    logging.error(f"Group {name} cannot include itself")
                    continue
                group = Group(name)
                group.activate()
                self.channels.extend(group.channels)

        self._is_initialized = True

    def activate(self) -> None:
        if not self._is_initialized:
            self._build_group()
