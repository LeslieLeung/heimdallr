from typing import List

from heimdallr.channel.base import Channel
from heimdallr.channel.factory import build_channel
from heimdallr.config.config import get_config_list, get_config_str
from heimdallr.config.definition import *


class Group:
    token: str
    channels: List[Channel] = []

    def __init__(self, name: str) -> None:
        self._build_group(name)

    def _build_group(self, name: str) -> None:
        # get enabled channels
        group_name = str.upper(name)
        enabled_channels = get_config_list(group_name, SUFFIX_ENABLED_CHANNELS, [])
        self.token = get_config_str(group_name, SUFFIX_TOKEN, "")

        for channel_name in enabled_channels:
            channel = build_channel(channel_name)
            self.channels.append(channel)
