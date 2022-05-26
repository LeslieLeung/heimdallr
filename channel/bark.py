from exception import ParamException

from .base import ChannelBase


class Bark(ChannelBase):
    def __init__(self):
        self.base_url = ""
        self.key = ""
        self.title = ""
        self.category = ""
        self.body = ""

    def compose_message(self) -> str:
        msg_string = ""
        if self.category != "":
            msg_string += f"/{self.category}"
        if self.title != "":
            msg_string += f" {self.title}"
        if self.body == "":
            raise ParamException("Message body cannot be empty.")
        else:
            msg_string += f" {self.body}"
        return msg_string

    def send(self, message):
        """
        Send a message to bark server.
        """
        pass
