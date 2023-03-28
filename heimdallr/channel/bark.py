import json
import logging
from urllib.parse import quote_plus

import requests

from env import get_env
from heimdallr.channel.base import Channel, Message
from heimdallr.exception import ParamException


class BarkMessage(Message):
    def __init__(self, title: str, body: str, category: str = "", param: str = "", jump_url: str = ""):
        super().__init__(title, body)
        self.category = category
        self.param = param
        self.jump_url = jump_url


class Bark(Channel):
    def __init__(self, message: BarkMessage):
        super().__init__(message, name="bark")
        self.base_url = ""
        self.key = ""
        self.get_credential()
        self.message = message

    def get_credential(self):
        env = get_env()
        self.base_url = env.bark_url
        self.key = env.bark_key
        if self.base_url == "" or self.key == "":
            raise ParamException("bark url or key not set")

    def compose_message(self) -> str:
        msg_string = ""
        if self.message.title != "":
            msg_string += f"/{quote_plus(self.message.title)}"
        if self.message.body == "":
            raise ParamException("Message body cannot be empty.")
        else:
            msg_string += f"/{quote_plus(self.message.body)}"
        if self.message.jump_url != "":
            msg_string += f"?url={quote_plus(self.message.jump_url)}"
        return msg_string

    def send(self):
        """
        Send a message to bark server.
        """
        url = f"{self.base_url}/{self.key}{self.compose_message()}"
        logging.info(f"Bark requested: {url}")
        rs = requests.get(url)
        logging.info(f"Bark response: {rs.text}")
        rs = json.loads(rs.text)
        if rs["code"] == 200:
            return True, rs["message"]
        return False, rs["message"]
