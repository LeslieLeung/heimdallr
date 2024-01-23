import logging
from typing import Tuple
from urllib.parse import quote_plus

import requests

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import SUFFIX_BARK_KEY, SUFFIX_BARK_URL
from heimdallr.exception import ParamException

logger = logging.getLogger(__name__)


class BarkMessage(Message):
    def __init__(
        self,
        title: str,
        body: str,
        category: str = "",
        param: str = "",
        jump_url: str = "",
        **kwargs,
    ):
        super().__init__(title, body)
        self.category = category
        self.param = param
        self.jump_url = jump_url

    def render_message(self) -> str:
        msg_string = ""
        if self.title != "":
            msg_string += f"/{quote_plus(self.title)}"
        if self.body == "":
            raise ParamException("Message body cannot be empty.")
        else:
            msg_string += f"/{quote_plus(self.body)}"
        if self.jump_url != "":
            msg_string += f"?url={quote_plus(self.jump_url)}"
        return msg_string


class Bark(Channel):
    def __init__(self, name: str, type: str) -> None:
        super().__init__(name, type)
        self.base_url: str = "https://api.day.app"
        self.key: str
        self._build_channel()

    def _build_channel(self) -> None:
        self.base_url = get_config_str(self.get_name(), SUFFIX_BARK_URL, self.base_url)
        self.key = get_config_str(self.get_name(), SUFFIX_BARK_KEY, "")
        if self.key == "":
            raise ParamException("Bark key cannot be empty.")

    def send(self, message: Message) -> Tuple[bool, str]:
        """
        Send a message to bark server.
        """
        url = f"{self.base_url}/{self.key}{message.render_message()}"
        rs = requests.get(url)
        logger.debug(f"Bark response: {rs.text}")
        rs_json = rs.json()
        if rs_json["code"] == 200:
            return True, rs_json["message"]
        logger.error(f"Bark error: {rs_json['message']}")
        return False, rs_json["message"]
