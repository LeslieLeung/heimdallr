import logging
from urllib.parse import quote

import requests

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import SUFFIX_PUSHDEER_TOKEN
from heimdallr.exception.param import ParamException

logger = logging.getLogger(__name__)


class PushDeerMessage(Message):
    def __init__(self, title: str, body: str, **kwargs):
        super().__init__(title, body)

    def render_message(self) -> str:
        return quote(f"{self.title}\n{self.body}")


class PushDeer(Channel):
    def __init__(self, name: str, type: str):
        super().__init__(name, type)
        self.base_url = "https://api2.pushdeer.com/message/push?"
        self.push_key: str
        self._build_channel()

    def _build_channel(self):
        self.push_key = get_config_str(
            self.get_config_name(), SUFFIX_PUSHDEER_TOKEN, ""
        )
        if self.push_key == "":
            raise ParamException("PushDeer token cannot be empty.")

    def send(self, message: Message):
        url = f"{self.base_url}pushkey={self.push_key}&text={message.render_message()}"
        rs = requests.post(url).json()
        if rs["code"] == 0:
            return True, rs["content"]
        logger.error(f"PushDeer error: {rs['error']}")
        return False, rs["error"]
