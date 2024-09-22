import logging
import smtplib
from contextlib import closing
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Union

from heimdallr.channel.base import Channel, Message
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import (
    SUFFIX_EMAIL_HOST,
    SUFFIX_EMAIL_PASSWORD,
    SUFFIX_EMAIL_PORT,
    SUFFIX_EMAIL_SENDER,
    SUFFIX_EMAIL_STARTTLS,
    SUFFIX_EMAIL_TO,
    SUFFIX_EMAIL_USER,
)
from heimdallr.exception import ParamException

logger = logging.getLogger(__name__)


class EmailMessage(Message):
    def __init__(self, title: str, body: str, **kwargs):
        super().__init__(title, body)
        self.sender: str
        self.user: str
        self.to: str

    def render_message(self) -> Any:
        message = MIMEMultipart()
        message["From"] = f"{self.sender} <{self.user}>"
        message["To"] = self.to
        message["Subject"] = self.title
        message.attach(MIMEText(self.body, "plain", "utf-8"))
        return message.as_string()


class Email(Channel):
    def __init__(self, name: str, type: str):
        super().__init__(name, type)
        self.host: str = ""
        self.port: int = 25
        self.user: str = ""
        self.password: str = ""
        self.sender: str = "Heimdallr"
        self.to: str = ""
        self.starttls: bool = False
        self.smtp_object: Union[smtplib.SMTP, None] = None
        self._build_channel()

    def _build_channel(self):
        self.host = get_config_str(self.get_name(), SUFFIX_EMAIL_HOST, "")
        self.port = int(get_config_str(self.get_name(), SUFFIX_EMAIL_PORT, "25"))
        self.user = get_config_str(self.get_name(), SUFFIX_EMAIL_USER, "")
        self.password = get_config_str(self.get_name(), SUFFIX_EMAIL_PASSWORD, "")
        self.sender = get_config_str(self.get_name(), SUFFIX_EMAIL_SENDER, "Heimdallr")
        self.to = get_config_str(self.get_name(), SUFFIX_EMAIL_TO, "")
        self.starttls = get_config_str(self.get_name(), SUFFIX_EMAIL_STARTTLS, "False") == "True"
        if self.host == "" or self.user == "" or self.password == "" or self.to == "":
            raise ParamException("email host, user, password or to not set")

    def send(self, message: Message):
        if not isinstance(message, EmailMessage):
            raise ParamException("message type error")
        message.sender = self.sender
        message.user = self.user
        message.to = self.to
        try:
            with closing(smtplib.SMTP(self.host, self.port)) as smtp_object:
                if self.starttls:
                    smtp_object.starttls()
                smtp_object.login(self.user, self.password)
                smtp_object.sendmail(self.user, self.to, message.render_message())
                logger.debug(f"Email sent to {self.to}")
        except smtplib.SMTPException as e:
            logger.error(f"Email send failed: {e}")
            return False, f"SMTPException: {e}"
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False, f"Exception: {e}"
        return True, "success"
