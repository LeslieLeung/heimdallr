import base64
import hashlib
import hmac
import logging
import time
import urllib.parse
from typing import Any, Tuple

import requests

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import (
    SUFFIX_DINGTALK_SAFE_WORDS,
    SUFFIX_DINGTALK_SECRET,
    SUFFIX_DINGTALK_TOKEN,
)
from heimdallr.exception import ParamException

logger = logging.getLogger(__name__)


class DingTalkMessage(Message):
    def __init__(self, title: str, body: str, msg_type: str = "text", **kwargs) -> None:
        super().__init__(title, body)
        self.msg_type: str = msg_type

    @staticmethod
    def _generate_signature(secret: str) -> Tuple[str, str]:
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode("utf-8")
        string_to_sign = "{}\n{}".format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode("utf-8")
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign, timestamp

    @staticmethod
    def _append_safe_words(input: str, safe_words: str) -> str:
        if safe_words == "":
            return input
        return f"{input}\n[{safe_words}]"

    def render_message(self, **kwargs) -> Any:
        safe_words = kwargs.get("safe_words", "")
        match self.msg_type:
            case "markdown":
                msg = {
                    "msgtype": "markdown",
                    "markdown": {
                        "title": f"{self.title}",
                        "text": self._append_safe_words(f"{self.title}\n{self.body}", safe_words),
                    },
                }
            case _:
                msg = {
                    "msgtype": "text",
                    "text": {"content": self._append_safe_words(f"{self.title}\n{self.body}", safe_words)},
                }
        return msg


class DingTalk(Channel):
    def __init__(self, name: str, type: str) -> None:
        super().__init__(name, type)
        self.base_url: str = "https://oapi.dingtalk.com/robot/send?access_token="
        self.token: str = ""
        self.safe_words: str = ""
        self.secret: str = ""
        self._build_channel()

    def _build_channel(self) -> None:
        self.token = get_config_str(self.get_name(), SUFFIX_DINGTALK_TOKEN, "")
        if self.token == "":
            raise ParamException("DingTalk key not set")
        self.safe_words = get_config_str(self.get_name(), SUFFIX_DINGTALK_SAFE_WORDS, "")
        self.secret = get_config_str(self.get_name(), SUFFIX_DINGTALK_SECRET, "")

        if self.safe_words == "" and self.secret == "":
            raise ParamException("DingTalk safe words or secret not set")
        if self.safe_words != "" and self.secret != "":
            raise ParamException("DingTalk safe words and secret cannot be set at the same time")

    def send(self, message: Message) -> Tuple[bool, str]:
        if not isinstance(message, DingTalkMessage):
            raise ParamException("Invalid message type")

        url = f"{self.base_url}{self.token}"
        if self.secret != "":
            sign, timestamp = message._generate_signature(self.secret)
            url = f"{url}&sign={sign}&timestamp={timestamp}"
        rs = requests.post(
            url,
            json=message.render_message(safe_words=self.safe_words),
            headers={"Content-Type": "application/json"},
        ).json()
        logger.debug(f"DingTalk response: {rs}")
        if rs["errcode"] != 0:
            logger.error(f"DingTalk error: {rs['errmsg']}")
            return False, rs["errmsg"]
        return True, rs["errmsg"]
