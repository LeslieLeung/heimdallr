# -*- coding:utf-8 -*-
import os

# Bark server url and key
ENV_BARK_URL = "BARK_URL"
ENV_BARK_KEY = "BARK_KEY"
# Wecom webhook key，see https://developer.work.weixin.qq.com/document/path/91770
ENV_WECOM_WEBHOOK_KEY = "WECOM_KEY"
# Wecom corpid and secret，see https://developer.work.weixin.qq.com/document/path/91039
ENV_WECOM_CORP_ID = "WECOM_CORP_ID"
ENV_WECOM_AGENT_ID = "WECOM_AGENT_ID"
ENV_WECOM_SECRET = "WECOM_SECRET"


class Env:
    def __init__(self):
        self.bark_url = os.environ.get(ENV_BARK_URL)
        self.bark_key = os.environ.get(ENV_BARK_KEY)
        self.wecom_webhook_key = os.environ.get(ENV_WECOM_WEBHOOK_KEY)
        self.wecom_corp_id = os.environ.get(ENV_WECOM_CORP_ID)
        self.wecom_agent_id = os.environ.get(ENV_WECOM_AGENT_ID)
        self.wecom_secret = os.environ.get(ENV_WECOM_SECRET)


def get_env():
    return Env()
