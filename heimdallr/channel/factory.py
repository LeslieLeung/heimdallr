import logging

from heimdallr.channel.apprise import Apprise, AppriseMessage
from heimdallr.channel.bark import Bark, BarkMessage
from heimdallr.channel.base import Channel, Message
from heimdallr.channel.chanify import Chanify, ChanifyMessage
from heimdallr.channel.dingtalk import DingTalk, DingTalkMessage
from heimdallr.channel.discord import DiscordWebhook, DiscordWebhookMessage
from heimdallr.channel.email import Email, EmailMessage
from heimdallr.channel.lark import LarkWebhook, LarkWebhookMessage
from heimdallr.channel.ntfy import Ntfy, NtfyMessage
from heimdallr.channel.pushdeer import PushDeer, PushDeerMessage
from heimdallr.channel.pushme import Pushme, PushmeMessage
from heimdallr.channel.pushover import Pushover, PushoverMessage
from heimdallr.channel.telegram import Telegram, TelegramMessage
from heimdallr.channel.wecom import (
    WecomApp,
    WecomAppMessage,
    WecomWebhook,
    WecomWebhookMessage,
)
from heimdallr.config.config import get_config_str
from heimdallr.config.definition import SUFFIX_TYPE
from heimdallr.exception import ParamException

logger = logging.getLogger(__name__)

# supported channels
CHANNEL_BARK = "bark"
CHANNEL_WECOM_WEBHOOK = "wecom_webhook"
CHANNEL_WECOM_APP = "wecom_app"
CHANNEL_PUSHOVER = "pushover"
CHANNEL_PUSHDEER = "pushdeer"
CHANNEL_CHANIFY = "chanify"
CHANNEL_EMAIL = "email"
CHANNEL_DISCORD_WEBHOOK = "discord_webhook"
CHANNEL_TELEGRAM = "telegram"
CHANNEL_NTFY = "ntfy"
CHANNEL_LARK_WEBHOOK = "lark_webhook"
CHANNEL_DINGTALK_WEBHOOK = "dingtalk_webhook"
CHANNEL_APPRISE = "apprise"
CHANNEL_PUSHME = "pushme"


def _get_channel_type_by_name(name: str) -> str:
    """
    Get the channel type by name.
    """
    return get_config_str(name, SUFFIX_TYPE, "")


def build_channel(name: str) -> Channel:
    """
    Build a channel instance by name.
    """
    channel_type = _get_channel_type_by_name(name)
    logger.debug(f"Building channel {name}, type {channel_type}")

    # build channel instance
    if channel_type == CHANNEL_BARK:
        return Bark(name, channel_type)
    elif channel_type == CHANNEL_WECOM_WEBHOOK:
        return WecomWebhook(name, channel_type)
    elif channel_type == CHANNEL_WECOM_APP:
        return WecomApp(name, channel_type)
    elif channel_type == CHANNEL_PUSHOVER:
        return Pushover(name, channel_type)
    elif channel_type == CHANNEL_PUSHDEER:
        return PushDeer(name, channel_type)
    elif channel_type == CHANNEL_CHANIFY:
        return Chanify(name, channel_type)
    elif channel_type == CHANNEL_EMAIL:
        return Email(name, channel_type)
    elif channel_type == CHANNEL_DISCORD_WEBHOOK:
        return DiscordWebhook(name, channel_type)
    elif channel_type == CHANNEL_TELEGRAM:
        return Telegram(name, channel_type)
    elif channel_type == CHANNEL_NTFY:
        return Ntfy(name, channel_type)
    elif channel_type == CHANNEL_LARK_WEBHOOK:
        return LarkWebhook(name, channel_type)
    elif channel_type == CHANNEL_DINGTALK_WEBHOOK:
        return DingTalk(name, channel_type)
    elif channel_type == CHANNEL_APPRISE:
        return Apprise(name, channel_type)
    elif channel_type == CHANNEL_PUSHME:
        return Pushme(name, channel_type)
    else:
        raise ParamException(f"Channel {name} type {channel_type} not supported.")


def build_message(name: str, title: str, body: str, **kwargs) -> Message:
    """
    Build a message instance by name.
    """
    channel_type = _get_channel_type_by_name(name)
    # build message instance
    if channel_type == CHANNEL_BARK:
        return BarkMessage(title, body, **kwargs)
    elif channel_type == CHANNEL_WECOM_WEBHOOK:
        return WecomWebhookMessage(title, body, **kwargs)
    elif channel_type == CHANNEL_WECOM_APP:
        return WecomAppMessage(title, body, **kwargs)
    elif channel_type == CHANNEL_PUSHOVER:
        return PushoverMessage(title, body, **kwargs)
    elif channel_type == CHANNEL_PUSHDEER:
        return PushDeerMessage(title, body, **kwargs)
    elif channel_type == CHANNEL_CHANIFY:
        return ChanifyMessage(title, body, **kwargs)
    elif channel_type == CHANNEL_EMAIL:
        return EmailMessage(title, body, **kwargs)
    elif channel_type == CHANNEL_DISCORD_WEBHOOK:
        return DiscordWebhookMessage(title, body, **kwargs)
    elif channel_type == CHANNEL_TELEGRAM:
        return TelegramMessage(title, body, **kwargs)
    elif channel_type == CHANNEL_NTFY:
        return NtfyMessage(title, body, **kwargs)
    elif channel_type == CHANNEL_LARK_WEBHOOK:
        return LarkWebhookMessage(title, body, **kwargs)
    elif channel_type == CHANNEL_DINGTALK_WEBHOOK:
        return DingTalkMessage(title, body, **kwargs)
    elif channel_type == CHANNEL_APPRISE:
        return AppriseMessage(title, body, **kwargs)
    elif channel_type == CHANNEL_PUSHME:
        return PushmeMessage(title, body, **kwargs)
    else:
        raise ParamException(f"Channel type {channel_type} not supported.")
