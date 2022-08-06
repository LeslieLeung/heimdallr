# -*- coding:utf-8 -*-

import json
from urllib.parse import urlencode

import requests

from channel.base import Channel, Message
from env import get_env
from exception import ParamException


class PushoverMessage(Message):
    def __init__(self, title: str, body: str):
        super().__init__(title, body)


class Pushover(Channel):
    def __init__(self, message: PushoverMessage):
        super().__init__(message, name="pushover")
        self.base_url = "https://api.pushover.net/1/messages.json"
        self.token = ""
        self.user = ""
        self.get_credential()
        self.message = message

    def get_credential(self):
        env = get_env()
        self.token = env.pushover_token
        self.user = env.pushover_user
        if self.token == "" or self.user == "":
            raise ParamException("pushover token or user not set")

    def compose_message(self) -> str:
        return urlencode(f"{self.message.title}\n{self.message.body}")

    def send(self):
        url = f"{self.base_url}?token={self.token}&user={self.user}&message={self.compose_message()}"
        rs = requests.post(url)
        rs = json.loads(rs.text)
        if rs["status"] == 1:
            return True, rs["request"]
        return False, rs["errors"]
