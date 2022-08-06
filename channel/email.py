import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union

from channel.base import Channel, Message
from env import get_env
from exception import ParamException, SMTPException


class EmailMessage(Message):
    def __init__(self, title: str, body: str):
        super().__init__(title, body)


class Email(Channel):
    def __init__(self, message: EmailMessage):
        super().__init__(message, name="email")
        self.host = ""
        self.port = 25
        self.user = ""
        self.password = ""
        self.sender = "Heimdallr"
        self.to = ""
        self.starttls = False
        self.smtp_object: Union[smtplib.SMTP, None] = None
        self.get_credential()
        self.message = message

    def get_credential(self):
        env = get_env()
        self.host = env.email_host
        self.port = env.email_port
        self.user = env.email_user
        self.password = env.email_password
        if env.email_sender != "":
            self.sender = env.email_sender
        self.to = env.email_to
        if env.email_starttls == "True":
            self.starttls = True
        if self.host == "" or self.user == "" or self.password == "" or self.to == "":
            raise ParamException("email host, user, password or to not set")
        try:
            self.smtp_object = smtplib.SMTP(self.host, self.port)
            if self.starttls:
                self.smtp_object.starttls()
            self.smtp_object.login(self.user, self.password)
        except smtplib.SMTPException as e:
            raise SMTPException(f"SMTPException: {e}")

    def compose_message(self):
        message = MIMEMultipart()
        message["From"] = f"{self.sender} <{self.user}>"
        message["To"] = self.to
        message["Subject"] = self.message.title
        message.attach(MIMEText(self.message.body, "plain", "utf-8"))
        logging.info(f"Email message body: {message.as_string()}")
        return message.as_string()

    def send(self):
        try:
            self.smtp_object.sendmail(self.user, self.to, self.compose_message())
        except smtplib.SMTPException as e:
            return False, f"SMTPException: {e}"
        finally:
            self.smtp_object.quit()
        return True, "success"
