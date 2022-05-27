# -*- coding:utf-8 -*-
import os

ENV_BARK_URL = "BARK_URL"
ENV_BARK_KEY = "BARK_KEY"
ENV_WECOM_KEY = "WECOM_KEY"


class Env:
    def __init__(self):
        self.bark_url = os.environ.get(ENV_BARK_URL)
        self.bark_key = os.environ.get(ENV_BARK_KEY)
        self.wecom_key = os.environ.get(ENV_WECOM_KEY)

def get_env():
    return Env()