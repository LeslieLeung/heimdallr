import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import (
    SUFFIX_EMAIL_HOST,
    SUFFIX_EMAIL_PASSWORD,
    SUFFIX_EMAIL_PORT,
    SUFFIX_EMAIL_SENDER,
    SUFFIX_EMAIL_TO,
    SUFFIX_EMAIL_USER,
)
from heimdallr.exception import ParamException, SMTPException


class EmailMessage(Message):
    sender: str
    user: str
    to: str

    def __init__(self, title: str, body: str):
        super().__init__(title, body)

    def render_message(self) -> Any:
        message = MIMEMultipart()
        message["From"] = f"{self.sender} <{self.user}>"
        message["To"] = self.to
        message["Subject"] = self.title
        message.attach(MIMEText(self.body, "plain", "utf-8"))
        logging.info(f"Email message body: {message.as_string()}")
        return message.as_string()


class Email(Channel):
    host: str = ""
    port: int = 25
    user: str = ""
    password: str = ""
    sender: str = "Heimdallr"
    to: str = ""
    starttls: bool = False
    smtp_object: smtplib.SMTP

    def __init__(self, name: str):
        super().__init__(name)
        self._build_channel()

    def _build_channel(self):
        self.host = get_config_str(self.get_config_name(), SUFFIX_EMAIL_HOST, "")
        self.port = int(get_config_str(self.get_config_name(), SUFFIX_EMAIL_PORT, "25"))
        self.user = get_config_str(self.get_config_name(), SUFFIX_EMAIL_USER, "")
        self.password = get_config_str(
            self.get_config_name(), SUFFIX_EMAIL_PASSWORD, ""
        )
        self.sender = get_config_str(
            self.get_config_name(), SUFFIX_EMAIL_SENDER, "Heimdallr"
        )
        self.to = get_config_str(self.get_config_name(), SUFFIX_EMAIL_TO, "")
        self.starttls = (
            get_config_str(self.get_config_name(), "starttls", "False") == "True"
        )
        if self.host == "" or self.user == "" or self.password == "" or self.to == "":
            raise ParamException("email host, user, password or to not set")
        try:
            self.smtp_object = smtplib.SMTP(self.host, self.port)
            if self.starttls:
                self.smtp_object.starttls()
            self.smtp_object.login(self.user, self.password)
        except smtplib.SMTPException as e:
            raise SMTPException(f"SMTPException: {e}")

    def send(self, message: Message):
        if not isinstance(message, EmailMessage):
            raise ParamException("message type error")
        message.sender = self.sender
        message.user = self.user
        message.to = self.to
        try:
            self.smtp_object.sendmail(self.user, self.to, message.render_message())
        except smtplib.SMTPException as e:
            return False, f"SMTPException: {e}"
        finally:
            self.smtp_object.quit()
        return True, "success"
