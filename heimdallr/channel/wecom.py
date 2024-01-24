import json
import logging
from typing import Any

import requests

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import (
    SUFFIX_WECOM_AGENT_ID,
    SUFFIX_WECOM_CORP_ID,
    SUFFIX_WECOM_KEY,
    SUFFIX_WECOM_SECRET,
)
from heimdallr.exception import WecomException

logger = logging.getLogger(__name__)


class WecomWebhookMessage(Message):
    def __init__(self, title: str, body: str, msg_type: str = "text", **kwargs):
        super().__init__(title, body)
        self.msg_type: str = msg_type

    def render_message(self) -> Any:
        match self.msg_type:
            case "markdown":
                msg = {
                    "msgtype": "markdown",
                    "markdown": {"content": f"{self.title}\n{self.body}"},
                }
            case _:
                msg = {
                    "msgtype": "text",
                    "text": {"content": f"{self.title}\n{self.body}"},
                }
        return json.dumps(msg)


class WecomAppMessage(Message):
    def __init__(self, title: str, body: str, msg_type: str = "text", **kwargs):
        super().__init__(title, body)
        self.msg_type = msg_type
        self.agent_id: int

    def render_message(self) -> Any:
        match self.msg_type:
            case "markdown":
                msg = {
                    "touser": "@all",
                    "msgtype": "markdown",
                    "agentid": self.agent_id,
                    "markdown": {"content": f"### {self.title}\n> {self.body}"},
                    "safe": 0,
                }
            case _:
                msg = {
                    "touser": "@all",
                    "msgtype": "text",
                    "agentid": self.agent_id,
                    "text": {"content": f"{self.title}\n{self.body}"},
                    "safe": 0,
                }
        return json.dumps(msg)


class WecomWebhook(Channel):
    def __init__(self, name: str, type: str):
        super().__init__(name, type)
        self.base_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="
        self.key: str = ""
        self._build_channel()

    def _build_channel(self) -> None:
        self.key = get_config_str(self.get_name(), SUFFIX_WECOM_KEY, "")
        if self.key == "":
            raise WecomException("WecomWebhook key not set")

    def send(self, message: Message):
        if not isinstance(message, WecomWebhookMessage):
            raise WecomException("Invalid message type")
        url = f"{self.base_url}{self.key}"
        rs = requests.post(
            url,
            data=message.render_message(),
            headers={"Content-Type": "application/json"},
        ).json()
        logger.debug(f"WecomWebhook response: {rs}")
        if rs["errcode"] == 0:
            return True, rs["errmsg"]
        logger.error(f"WecomWebhook error: {rs['errmsg']}")
        return False, rs["errmsg"]


class WecomApp(Channel):
    def __init__(self, name: str, type: str):
        super().__init__(name, type)
        self.base_url: str = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
        self.corp_id: str
        self.secret: str
        self.access_token: str
        self.agent_id: int
        self._build_channel()

    def _build_channel(self) -> None:
        self.corp_id = get_config_str(self.get_name(), SUFFIX_WECOM_CORP_ID, "")
        self.secret = get_config_str(self.get_name(), SUFFIX_WECOM_SECRET, "")
        self.agent_id = int(get_config_str(self.get_name(), SUFFIX_WECOM_AGENT_ID, ""))

        if self.corp_id == "" or self.secret == "":
            raise WecomException("corp id or secret not set")

    def send(self, message: Message):
        if not isinstance(message, WecomAppMessage):
            raise WecomException("Invalid message type")
        # get access token
        auth_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corp_id}&corpsecret={self.secret}"
        rs = requests.get(auth_url, timeout=5).json()
        if rs["errcode"] == 0:
            self.access_token = rs["access_token"]
        else:
            raise WecomException(f"Failed to get access token: {rs['errmsg']}")
        # patch up message
        message.agent_id = self.agent_id
        msg = message.render_message()
        url = f"{self.base_url}{self.access_token}"
        rs = requests.post(
            url,
            data=msg,
            headers={"Content-Type": "application/json"},
        ).json()
        logger.debug(f"WecomApp response: {rs}")
        if rs["errcode"] == 0:
            return True, rs["errmsg"]
        logger.error(f"WecomApp error: {rs['errmsg']}")
        return False, rs["errmsg"]
