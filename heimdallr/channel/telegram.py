import logging
from typing import Tuple

import requests

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import SUFFIX_TELEGRAM_CHAT_ID, SUFFIX_TELEGRAM_TOKEN
from heimdallr.exception import ParamException

logger = logging.getLogger(__name__)


class TelegramMessage(Message):
    def __init__(self, title: str, body: str, **kwargs):
        super().__init__(title, body)

    def render_message(self) -> str:
        return f"{self.title}\n{self.body}"


class Telegram(Channel):
    def __init__(self, name: str, type: str):
        super().__init__(name, type)
        self.base_url = "https://api.telegram.org/bot"
        self.token: str
        self.chat_id: str
        self._build_channel()

    def _build_channel(self) -> None:
        self.token = get_config_str(self.get_config_name(), SUFFIX_TELEGRAM_TOKEN, "")
        self.chat_id = get_config_str(self.get_config_name(), SUFFIX_TELEGRAM_CHAT_ID, "")
        if not self.token or not self.chat_id:
            raise ParamException("Telegram token or chat id is empty.")

    def send(self, message: Message) -> Tuple[bool, str]:
        if not isinstance(message, TelegramMessage):
            raise ParamException("Telegram only supports TelegramMessage.")
        msg = {"chat_id": self.chat_id, "text": message.render_message()}
        url = f"{self.base_url}{self.token}/sendMessage"
        rs = requests.post(url, json=msg)
        if rs.status_code != 200:
            logger.error(f"Telegram send failed: {rs.text}")
        return rs.status_code == 200, rs.text
