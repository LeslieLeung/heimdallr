# -*- coding:utf-8 -*-

from .base import Channel, Message

class WecomMessage(Message):
    def __init__(self):
        super().__init__()


class Wecom(Channel):
    def __init__(self):
        super().__init__(name="wecom")

    def send(self):
        super().send()

    def get_credential(self):
        super().get_credential()

