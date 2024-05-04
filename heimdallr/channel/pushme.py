import logging
from typing import Mapping, Tuple

import requests

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import SUFFIX_PUSHME_PUSH_KEY, SUFFIX_PUSHME_URL
from heimdallr.exception import ParamException

logger = logging.getLogger(__name__)


class PushmeMessage(Message):
    def __init__(self, title: str, body: str, **kwargs) -> None:
        super().__init__(title, body)

    def render_message(self) -> Mapping[str, str]:
        return {"title": self.title, "contents": self.body}


class Pushme(Channel):
    def __init__(self, name: str, type: str) -> None:
        super().__init__(name, type)
        self.base_url: str = "https://push.i-i.me"
        self.push_key: str
        self._build_channel()

    def _build_channel(self) -> None:
        self.base_url = get_config_str(self.get_name(), SUFFIX_PUSHME_URL, self.base_url)
        self.push_key = get_config_str(self.get_name(), SUFFIX_PUSHME_PUSH_KEY, "")
        if self.push_key == "":
            raise ParamException("Pushme push key cannot be empty.")

    def send(self, message: Message) -> Tuple[bool, str]:
        """
        Send a message to pushme server.
        """
        param = message.render_message()
        param["push_key"] = self.push_key
        rs = requests.get(self.base_url, params=param)
        if rs.status_code != 200:
            logger.error(f"Pushme send failed: {rs.text}")
        return rs.status_code == 200, rs.text
