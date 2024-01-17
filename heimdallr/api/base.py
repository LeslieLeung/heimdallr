import asyncio
import logging
from typing import Dict

from heimdallr.channel.factory import build_message
from heimdallr.exception.auth import AuthException
from heimdallr.response import Response, success
from heimdallr.shared.config import config

logger = logging.getLogger(__name__)


def serve(key: str, title: str = "", body: str = "", **kwargs):
    try:
        group = config.get_group(key)
    except AuthException as e:
        return Response(code=-1, message=str(e)).render()
    logger.info(f"group: {group.name}, token: {group.token}")
    errors = {}
    for chan in group.channels:
        logger.info(f"channel: {chan.get_name()}, channel_type: {chan.get_type()}")
        message = build_message(chan.get_name(), title, body, **kwargs)
        rs, msg = chan.send(message)
        if not rs:
            errors[chan.get_name()] = msg

    if len(errors) == 0:
        return success()
    err_msg = ""
    for err in errors.items():
        err_msg += f"{err[0]} return: {err[1]}."
    return Response(code=1, message=err_msg).render()


async def serve_channels_async(key: str, title: str = "", body: str = "", **kwargs):
    try:
        group = config.get_group(key)
    except AuthException as e:
        return Response(code=-1, message=str(e)).render()
    logger.info(f"group: {group.name}, token: {group.token}")
    errors: Dict[str, str] = {}
    async with asyncio.TaskGroup() as tg:
        for chan in group.channels:
            tg.create_task(send_to_channel(chan, title, body, errors, kwargs))

    if len(errors) == 0:
        return success()
    err_msg = ""
    for err in errors.items():
        err_msg += f"{err[0]} return: {err[1]}."
    return Response(code=1, message=err_msg).render()


async def send_to_channel(chan, title, body, errors, kwargs):
    logger.info(f"channel: {chan.get_name()}, channel_type: {chan.get_type()}")
    message = build_message(chan.get_name(), title, body, **kwargs)
    rs, err = chan.send(message)
    if not rs:
        errors[chan.get_name()] = err
