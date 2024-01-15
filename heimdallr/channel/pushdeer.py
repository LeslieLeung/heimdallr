import logging
from urllib.parse import quote

import requests

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import SUFFIX_PUSHDEER_TOKEN
from heimdallr.exception.param_exception import ParamException


class PushDeerMessage(Message):
    def __init__(self, title: str, body: str):
        super().__init__(title, body)

    def render_message(self) -> str:
        return quote(f"{self.title}\n{self.body}")


class PushDeer(Channel):
    base_url = "https://api2.pushdeer.com/message/push?"
    push_key = ""

    def __init__(self, name: str):
        super().__init__(name)
        self._build_channel()

    def _build_channel(self):
        self.push_key = get_config_str(
            self.get_config_name(), SUFFIX_PUSHDEER_TOKEN, ""
        )
        if self.push_key == "":
            raise ParamException("PushDeer token cannot be empty.")

    def send(self, message: Message):
        url = f"{self.base_url}pushkey={self.push_key}&text={message.render_message()}"
        logging.info(f"PushDeer requested: {url}")
        rs = requests.post(url).json()
        if rs["code"] == 0:
            return True, rs["content"]
        return False, rs["error"]
