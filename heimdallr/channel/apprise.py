from typing import Tuple

import apprise

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import SUFFIX_APPRISE_URL
from heimdallr.exception import ParamException


class AppriseMessage(Message):
    def __init__(
        self,
        title: str,
        body: str,
        **kwargs,
    ):
        super().__init__(title, body)

    def render_message(self) -> str:
        return self.body


class Apprise(Channel):
    def __init__(self, name: str, type: str) -> None:
        super().__init__(name, type)
        self.url: str
        self._build_channel()

    def _build_channel(self) -> None:
        self.url = get_config_str(self.get_name(), SUFFIX_APPRISE_URL, "")
        if self.url == "":
            raise ParamException("Apprise url cannot be empty.")

    def send(self, message: Message) -> Tuple[bool, str]:
        """
        Send a message to apprise server.
        """
        ap = apprise.Apprise()
        ap.add(self.url)
        try:
            ap.notify(
                body=message.render_message(),
                title=message.title,
            )
            return True, ""
        except Exception as e:
            return False, str(e)
