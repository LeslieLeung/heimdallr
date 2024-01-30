import logging
from typing import Any, Tuple

import requests

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import SUFFIX_LARK_HOST, SUFFIX_LARK_TOKEN
from heimdallr.exception import ParamException

logger = logging.getLogger(__name__)


class LarkWebhookMessage(Message):
    def __init__(self, title: str, body: str, **kwargs) -> None:
        super().__init__(title, body)

    def render_message(self) -> Any:
        return {"msg_type": "text", "content": {"text": f"{self.title}\n{self.body}"}}


class LarkWebhook(Channel):
    def __init__(self, name: str, type: str) -> None:
        super().__init__(name, type)
        self.base_url: str = "https://open.feishu.cn/open-apis/bot/v2/hook/"
        self.token: str = ""
        self._build_channel()

    def _build_channel(self) -> None:
        self.base_url = get_config_str(self.get_name(), SUFFIX_LARK_HOST, self.base_url)
        self.token = get_config_str(self.get_name(), SUFFIX_LARK_TOKEN, "")
        if self.token == "":
            raise ParamException("LarkWebhook key not set")

    def send(self, message: Message) -> Tuple[bool, str]:
        if not isinstance(message, LarkWebhookMessage):
            raise ParamException("Invalid message type")

        url = f"{self.base_url}{self.token}"
        rs = requests.post(
            url,
            json=message.render_message(),
            headers={"Content-Type": "application/json"},
        ).json()
        logger.debug(f"LarkWebhook response: {rs}")
        if rs["code"] != 0:
            logger.error(f"LarkWebhook error: {rs['msg']}")
            return False, rs["msg"]
        return True, rs["msg"]
