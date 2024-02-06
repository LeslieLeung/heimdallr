import logging
from typing import Any, Tuple

import requests

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import (
    SUFFIX_DINGTALK_SAFE_WORDS,
    SUFFIX_DINGTALK_TOKEN,
)
from heimdallr.exception import ParamException

logger = logging.getLogger(__name__)


class DingTalkMessage(Message):
    def __init__(self, title: str, body: str, msg_type: str = "text", **kwargs) -> None:
        super().__init__(title, body)
        self.msg_type: str = msg_type

    def render_message(self, **kwargs) -> Any:
        safe_words = kwargs.get("safe_words", "")
        match self.msg_type:
            case "markdown":
                msg = {
                    "msgtype": "markdown",
                    "markdown": {
                        "title": f"{self.title}",
                        "text": f"{self.title}\n{self.body}\n[{safe_words}]",
                    },
                }
            case _:
                msg = {
                    "msgtype": "text",
                    "text": {"content": f"{self.title}\n{self.body}\n[{safe_words}]"},
                }
        return msg


class DingTalk(Channel):
    def __init__(self, name: str, type: str) -> None:
        super().__init__(name, type)
        self.base_url: str = "https://oapi.dingtalk.com/robot/send?access_token="
        self.token: str = ""
        self.safe_words: str = ""
        self._build_channel()

    def _build_channel(self) -> None:
        self.token = get_config_str(self.get_name(), SUFFIX_DINGTALK_TOKEN, "")
        if self.token == "":
            raise ParamException("DingTalk key not set")
        self.safe_words = get_config_str(self.get_name(), SUFFIX_DINGTALK_SAFE_WORDS, "")
        if self.safe_words == "":
            raise ParamException("DingTalk safe words not set")

    def send(self, message: Message) -> Tuple[bool, str]:
        if not isinstance(message, DingTalkMessage):
            raise ParamException("Invalid message type")

        url = f"{self.base_url}{self.token}"
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
