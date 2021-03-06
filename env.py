# -*- coding:utf-8 -*-
import os

# debug mode
ENV_DEBUG = "DEBUG"
# Bark server url and key
ENV_BARK_URL = "BARK_URL"
ENV_BARK_KEY = "BARK_KEY"
# Wecom webhook key，see https://developer.work.weixin.qq.com/document/path/91770
ENV_WECOM_WEBHOOK_KEY = "WECOM_KEY"
# Wecom corpid and secret，see https://developer.work.weixin.qq.com/document/path/91039
ENV_WECOM_CORP_ID = "WECOM_CORP_ID"
ENV_WECOM_AGENT_ID = "WECOM_AGENT_ID"
ENV_WECOM_SECRET = "WECOM_SECRET"
# Pushover, see https://pushover.net/api
ENV_PUSHOVER_TOKEN = "PUSHOVER_TOKEN"
ENV_PUSHOVER_USER = "PUSHOVER_USER"
# PushDeer, see http://pushdeer.com/
ENV_PUSHDEER_TOKEN = "PUSHDEER_TOKEN"
# Chanify, see https://github.com/chanify/chanify
ENV_CHANIFY_ENDPOINT = "CHANIFY_ENDPOINT"
ENV_CHANIFY_TOKEN = "CHANIFY_TOKEN"
# SMTP mail
ENV_EMAIL_HOST = "EMAIL_HOST"
ENV_EMAIL_PORT = "EMAIL_PORT"
ENV_EMAIL_USER = "EMAIL_USER"
ENV_EMAIL_PASSWORD = "EMAIL_PASSWORD"
ENV_EMAIL_SENDER = "EMAIL_SENDER"
ENV_EMAIL_TO = "EMAIL_TO"
ENV_EMAIL_STARTTLS = "EMAIL_STARTTLS"
# Access token for Docker deployment
ENV_KEY = "KEY"


class Env:
    def __init__(self):
        self.debug = os.environ.get("DEBUG", False)
        self.bark_url = os.environ.get(ENV_BARK_URL, "")
        self.bark_key = os.environ.get(ENV_BARK_KEY, "")
        self.wecom_webhook_key = os.environ.get(ENV_WECOM_WEBHOOK_KEY, "")
        self.wecom_corp_id = os.environ.get(ENV_WECOM_CORP_ID, "")
        self.wecom_agent_id = os.environ.get(ENV_WECOM_AGENT_ID, "")
        self.wecom_secret = os.environ.get(ENV_WECOM_SECRET, "")
        self.pushover_token = os.environ.get(ENV_PUSHOVER_TOKEN, "")
        self.pushover_user = os.environ.get(ENV_PUSHOVER_USER, "")
        self.pushdeer_token = os.environ.get(ENV_PUSHDEER_TOKEN, "")
        self.chanify_endpoint = os.environ.get(ENV_CHANIFY_ENDPOINT, "")
        self.chanify_token = os.environ.get(ENV_CHANIFY_TOKEN, "")
        self.email_host = os.environ.get(ENV_EMAIL_HOST, "")
        self.email_port = os.environ.get(ENV_EMAIL_PORT, "")
        self.email_user = os.environ.get(ENV_EMAIL_USER, "")
        self.email_password = os.environ.get(ENV_EMAIL_PASSWORD, "")
        self.email_sender = os.environ.get(ENV_EMAIL_SENDER, "")
        self.email_to = os.environ.get(ENV_EMAIL_TO, "")
        self.email_starttls = os.environ.get(ENV_EMAIL_STARTTLS, "")
        self.key = os.environ.get(ENV_KEY, "")


def get_env():
    return Env()


def is_debug():
    return get_env().debug
