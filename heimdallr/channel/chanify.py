import logging
from typing import Any
from urllib.parse import quote_plus

import requests

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import SUFFIX_CHANIFY_ENDPOINT, SUFFIX_CHANIFY_TOKEN
from heimdallr.exception import ParamException

logger = logging.getLogger(__name__)


class ChanifyMessage(Message):
    def __init__(self, title: str, body: str):
        super().__init__(title, body)

    def render_message(self) -> Any:
        return quote_plus(f"{self.title}\n{self.body}")


class Chanify(Channel):
    def __init__(self, name: str):
        super().__init__(name)
        self.base_url: str = "https://api.chanify.net/v1/sender"
        self.token: str
        self._build_channel()

    def _build_channel(self) -> None:
        self.base_url = get_config_str(
            self.get_config_name(), SUFFIX_CHANIFY_ENDPOINT, self.base_url
        )
        self.token = get_config_str(self.get_config_name(), SUFFIX_CHANIFY_TOKEN, "")
        if self.token == "":
            raise ParamException("chanify token not set")

    def send(self, message: Message):
        url = f"{self.base_url}/{self.token}/{message.render_message()}"
        logger.info(f"Chanify requested: {url}")
        rs = requests.get(url).json()
        if "request-uid" in rs:
            return True, "success"
        return False, rs["msg"]
