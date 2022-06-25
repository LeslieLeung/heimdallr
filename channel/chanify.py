import json
import logging
from urllib.parse import quote_plus

import requests

from env import get_env
from exception import ParamException

from .base import Channel, Message


class ChanifyMessage(Message):
    def __init__(self, title: str, body: str):
        super().__init__(title, body)


class Chanify(Channel):
    def __init__(self, message: ChanifyMessage):
        super().__init__(message, name="chanify")
        self.base_url = "https://api.chanify.net/v1/sender"
        self.token = ""
        self.get_credential()
        self.message = message

    def get_credential(self):
        env = get_env()
        self.token = env.chanify_token
        if self.token == "":
            raise ParamException("chanify token not set")
        if env.chanify_endpoint != "":
            self.base_url = env.chanify_endpoint

    def compose_message(self) -> str:
        return quote_plus(f"{self.message.title}\n{self.message.body}")

    def send(self):
        url = f"{self.base_url}/{self.token}/{self.compose_message()}"
        logging.info(f"Chanify requested: {url}")
        rs = requests.get(url)
        logging.info(f"Chanify response: {rs.text}")
        rs = json.loads(rs.text)
        if "request-uid" in rs:
            return True, "success"
        return False, rs["msg"]
