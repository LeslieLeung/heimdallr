# -*- coding:utf-8 -*-

from env import get_env
from exception import ParamException
from urllib.parse import urlencode

import requests
import json

from .base import Channel, Message

class PushDeerMessage(Message):
    def __init__(self, title: str, body: str):
        super().__init__(title, body)


class PushDeer(Channel):
    def __init__(self, message: PushDeerMessage):
        super().__init__(message, name="pushdeer")
        self.base_url = "https://api2.pushdeer.com/message/push?"
        self.pushkey = ""
        self.get_credential()
        self.message = message

    def get_credential(self):
        env = get_env()
        self.pushkey = env.pushdeer_pushkey
        if self.pushkey == "":
            raise ParamException("pushdeer pushkey not set")

    def compose_message(self) -> str:
        return urlencode(f"{self.message.title}\n{self.message.body}")

    def send(self):
        url = f"{self.base_url}pushkey={self.pushkey}&text={self.compose_message()}"
        rs = requests.post(url)
        rs = json.loads(rs.text)
        if rs["code"] == 0:
            return True, rs["content"]
        return False, rs["error"]