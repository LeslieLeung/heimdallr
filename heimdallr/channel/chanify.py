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
    def __init__(self, title: str, body: str, **kwargs):
        super().__init__(title, body)

    def render_message(self) -> Any:
        return quote_plus(f"{self.title}\n{self.body}")


class Chanify(Channel):
    def __init__(self, name: str, type: str):
        super().__init__(name, type)
        self.base_url: str = "https://api.chanify.net/v1/sender"
        self.token: str
        self._build_channel()

    def _build_channel(self) -> None:
        self.base_url = get_config_str(self.get_config_name(), SUFFIX_CHANIFY_ENDPOINT, self.base_url)
        self.token = get_config_str(self.get_config_name(), SUFFIX_CHANIFY_TOKEN, "")
        if self.token == "":
            raise ParamException("chanify token not set")

    def send(self, message: Message):
        url = f"{self.base_url}/{self.token}/{message.render_message()}"
        rs = requests.get(url).json()
        logger.debug(f"Chanify response: {rs}")
        if "request-uid" in rs:
            return True, "success"
        logger.error(f"Chanify error: {rs['msg']}")
        return False, rs["msg"]
