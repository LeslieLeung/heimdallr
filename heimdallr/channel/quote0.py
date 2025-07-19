import logging
from typing import Tuple

import requests

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import (
    SUFFIX_QUOTE0_API_KEY,
    SUFFIX_QUOTE0_BASE_URL,
    SUFFIX_QUOTE0_DEVICE_ID,
)
from heimdallr.exception import ParamException

logger = logging.getLogger(__name__)


class Quote0Message(Message):
    def __init__(
        self,
        title: str,
        body: str,
        **kwargs,
    ):
        super().__init__(title, body)

    def render_message(self) -> dict:
        """
        Render the message to the format that MindReset API expects.
        According to the API docs: https://dot.mindreset.tech/docs/server/text_api
        The API expects: POST /api/open/text
        Header: "Authorization: Bearer <API_KEY>"
        Body: {"deviceId":"<序列号>","title":"<标题>","message":"<内容>"}
        """
        if self.body == "":
            raise ParamException("Message body cannot be empty.")

        payload = {"deviceId": "", "title": self.title, "message": self.body, "signature": "Heimdallr"}
        return payload


class Quote0(Channel):
    def __init__(self, name: str, type: str) -> None:
        super().__init__(name, type)
        self.base_url: str = "https://dot.mindreset.tech"
        self.device_id: str = ""
        self.api_key: str = ""
        self._build_channel()

    def _build_channel(self) -> None:
        """
        Get the configuration for Quote0 channel.
        """
        self.base_url = get_config_str(self.get_name(), SUFFIX_QUOTE0_BASE_URL, self.base_url)
        self.device_id = get_config_str(self.get_name(), SUFFIX_QUOTE0_DEVICE_ID, "")
        self.api_key = get_config_str(self.get_name(), SUFFIX_QUOTE0_API_KEY, "")

        if self.device_id == "":
            raise ParamException("Quote0 device ID cannot be empty.")
        if self.api_key == "":
            raise ParamException("Quote0 API key cannot be empty.")

    def send(self, message: Message) -> Tuple[bool, str]:
        """
        Send a message to MindReset server.
        According to API docs: POST /api/open/text
        """
        if not isinstance(message, Quote0Message):
            message = Quote0Message(message.title, message.body)

        url = f"{self.base_url}/api/open/text"
        payload = message.render_message()
        payload["deviceId"] = self.device_id

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        try:
            rs = requests.post(url, json=payload, headers=headers)
            logger.debug(f"Quote0 response: {rs.text}")

            # Check if the request was successful
            if rs.status_code == 200:
                return True, "Message sent successfully"
            else:
                error_msg = f"HTTP {rs.status_code}: {rs.text}"
                logger.error(f"Quote0 error: {error_msg}")
                return False, error_msg

        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(f"Quote0 request error: {error_msg}")
            return False, error_msg
