# -*- coding:utf-8 -*-
import json
import os
from typing import Any

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
        self.debug = False
        self.bark_url = ""
        self.bark_key = ""
        self.wecom_webhook_key = ""
        self.wecom_corp_id = ""
        self.wecom_agent_id = ""
        self.wecom_secret = ""
        self.pushover_token = ""
        self.pushover_user = ""
        self.pushdeer_token = ""
        self.chanify_endpoint = ""
        self.chanify_token = ""
        self.email_host = ""
        self.email_port = ""
        self.email_user = ""
        self.email_password = ""
        self.email_sender = ""
        self.email_to = ""
        self.email_starttls = ""
        self.key = ""
        self.get_config()
        self.get_config_from_env()

    def get_config(self):
        if os.path.exists("./config/config.json"):
            with open("./config/config.json", "r") as f:
                config = json.load(f)
            self.bark_url = get_config_key(config, ENV_BARK_URL.lower())
            self.bark_key = get_config_key(config, ENV_BARK_KEY.lower())
            self.wecom_webhook_key = get_config_key(
                config, ENV_WECOM_WEBHOOK_KEY.lower()
            )
            self.wecom_corp_id = get_config_key(config, ENV_WECOM_CORP_ID.lower())
            self.wecom_agent_id = get_config_key(config, ENV_WECOM_AGENT_ID.lower())
            self.wecom_secret = get_config_key(config, ENV_WECOM_SECRET.lower())
            self.pushover_token = get_config_key(config, ENV_PUSHOVER_TOKEN.lower())
            self.pushover_user = get_config_key(config, ENV_PUSHOVER_USER.lower())
            self.pushdeer_token = get_config_key(config, ENV_PUSHDEER_TOKEN.lower())
            self.chanify_endpoint = get_config_key(config, ENV_CHANIFY_ENDPOINT.lower())
            self.chanify_token = get_config_key(config, ENV_CHANIFY_TOKEN.lower())
            self.email_host = get_config_key(config, ENV_EMAIL_HOST.lower())
            self.email_port = get_config_key(config, ENV_EMAIL_PORT.lower())
            self.email_user = get_config_key(config, ENV_EMAIL_USER.lower())
            self.email_password = get_config_key(config, ENV_EMAIL_PASSWORD.lower())
            self.email_sender = get_config_key(config, ENV_EMAIL_SENDER.lower())
            self.email_to = get_config_key(config, ENV_EMAIL_TO.lower())
            self.email_starttls = get_config_key(config, ENV_EMAIL_STARTTLS.lower())
            self.key = get_config_key(config, ENV_KEY.lower())

    def get_config_from_env(self):
        self.debug = os.environ.get("DEBUG", False)
        if self.bark_url == "":
            self.bark_url = os.environ.get(ENV_BARK_URL, "")
        if self.bark_key == "":
            self.bark_key = os.environ.get(ENV_BARK_KEY, "")
        if self.wecom_webhook_key == "":
            self.wecom_webhook_key = os.environ.get(ENV_WECOM_WEBHOOK_KEY, "")
        if self.wecom_corp_id == "":
            self.wecom_corp_id = os.environ.get(ENV_WECOM_CORP_ID, "")
        if self.wecom_agent_id == "":
            self.wecom_agent_id = os.environ.get(ENV_WECOM_AGENT_ID, "")
        if self.wecom_secret == "":
            self.wecom_secret = os.environ.get(ENV_WECOM_SECRET, "")
        if self.pushover_token == "":
            self.pushover_token = os.environ.get(ENV_PUSHOVER_TOKEN, "")
        if self.pushover_user == "":
            self.pushover_user = os.environ.get(ENV_PUSHOVER_USER, "")
        if self.pushdeer_token == "":
            self.pushdeer_token = os.environ.get(ENV_PUSHDEER_TOKEN, "")
        if self.chanify_endpoint == "":
            self.chanify_endpoint = os.environ.get(ENV_CHANIFY_ENDPOINT, "")
        if self.chanify_token == "":
            self.chanify_token = os.environ.get(ENV_CHANIFY_TOKEN, "")
        if self.email_host == "":
            self.email_host = os.environ.get(ENV_EMAIL_HOST, "")
        if self.email_port == "":
            self.email_port = os.environ.get(ENV_EMAIL_PORT, "")
        if self.email_user == "":
            self.email_user = os.environ.get(ENV_EMAIL_USER, "")
        if self.email_password == "":
            self.email_password = os.environ.get(ENV_EMAIL_PASSWORD, "")
        if self.email_sender == "":
            self.email_sender = os.environ.get(ENV_EMAIL_SENDER, "")
        if self.email_to == "":
            self.email_to = os.environ.get(ENV_EMAIL_TO, "")
        if self.email_starttls == "":
            self.email_starttls = os.environ.get(ENV_EMAIL_STARTTLS, "")
        if self.key == "":
            self.key = os.environ.get(ENV_KEY, "")


def get_env():
    return Env()


def get_config_key(config_dict: dict, key: str, default: Any = ""):
    try:
        return config_dict[key]
    except KeyError:
        return default


def is_debug():
    return get_env().debug
