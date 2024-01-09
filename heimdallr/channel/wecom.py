import json
import logging

import requests

from env import get_env
from heimdallr.channel.base import Channel, Message
from heimdallr.exception import WecomException


class WecomMessage(Message):
    def __init__(self, title: str, body: str, msg_type: str = "text"):
        super().__init__(title, body)
        self.msg_type = msg_type


class WecomWebhook(Channel):
    def __init__(self, message: WecomMessage):
        super().__init__(message, name="wecom webhook")
        self.base_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="
        self.key = ""
        self.get_credential()

    def compose_message(self) -> str:
        assert isinstance(self.message, WecomMessage), "message type error"
        match self.message.msg_type:
            case "text":
                msg = {
                    "msgtype": "text",
                    "text": {"content": f"{self.message.title}\n{self.message.body}"},
                }
            case "markdown":
                msg = {
                    "msgtype": "markdown",
                    "markdown": {
                        "content": f"### {self.message.title}\n> {self.message.body}"
                    },
                }
            case _:
                raise WecomException("Unsupported message type")
        return json.dumps(msg)

    def send(self):
        super().send()
        url = f"{self.base_url}{self.key}"
        logging.info(
            f"WecomWebhook requested: {url}, with message: {self.compose_message()}"
        )
        rs = requests.post(
            url,
            data=self.compose_message(),
            headers={"Content-Type": "application/json"},
        )
        logging.info(f"WecomWebhook response: {rs.text}")
        rs = json.loads(rs.text)
        if rs["errcode"] == 0:
            return True, rs["errmsg"]
        return False, rs["errmsg"]

    def get_credential(self):
        env = get_env()
        self.key = env.wecom_webhook_key


class WecomApp(Channel):
    def __init__(self, message: WecomMessage):
        super().__init__(message, name="wecom app")
        self.base_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
        self.access_token = ""
        self.agent_id = ""
        self.get_credential()

    def compose_message(self) -> str:
        assert isinstance(self.message, WecomMessage), "message type error"
        match self.message.msg_type:
            case "text":
                msg = {
                    "touser": "@all",
                    "msgtype": "text",
                    "agentid": self.agent_id,
                    "text": {"content": f"{self.message.title}\n{self.message.body}"},
                    "safe": 0,
                }
            case "markdown":
                msg = {
                    "touser": "@all",
                    "msgtype": "markdown",
                    "agentid": self.agent_id,
                    "markdown": {
                        "content": f"### {self.message.title}\n> {self.message.body}"
                    },
                    "safe": 0,
                }
            case _:
                raise WecomException("Unsupported message type")
        return json.dumps(msg)

    def send(self):
        msg = self.compose_message()
        url = f"{self.base_url}{self.access_token}"
        logging.info(f"WecomApp requested: {url}, with message: {msg}")
        rs = requests.post(
            url,
            data=msg,
            headers={"Content-Type": "application/json"},
        )
        logging.info(f"WecomApp response: {rs.text}")
        rs = json.loads(rs.text)
        if rs["errcode"] == 0:
            return True, rs["errmsg"]
        return False, rs["errmsg"]

    def get_credential(self):
        env = get_env()
        self.agent_id = env.wecom_agent_id
        if self.agent_id == "":
            raise WecomException("agent id not set")
        corp_id, secret = env.wecom_corp_id, env.wecom_secret
        if corp_id == "" or secret == "":
            raise WecomException("corp id or secret not set")
        auth_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={secret}"
        rs = requests.get(auth_url)
        rs = json.loads(rs.text)
        if rs["errcode"] == 0:
            self.access_token = rs["access_token"]
        else:
            raise WecomException(f"Failed to get access token: {rs['errmsg']}")
