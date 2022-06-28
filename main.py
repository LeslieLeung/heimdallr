import logging

from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from channel import (
    Bark,
    BarkMessage,
    Chanify,
    ChanifyMessage,
    Email,
    EmailMessage,
    PushDeer,
    PushDeerMessage,
    Pushover,
    PushoverMessage,
    WecomApp,
    WecomMessage,
    WecomWebhook,
)
from env import get_env, is_debug
from exception import ParamException, WecomException

app = FastAPI()

if is_debug():
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.ERROR)


class PostRequest(BaseModel):
    channel: str
    title: str = ""
    body: str = ""
    key: str = ""


@app.get("/{channel}")
@app.get("/{channel}/{title}/{body}")
@app.post("/{channel}/{title}/{body}")
@app.get("/{channel}/{title}/{body}/{key}")
@app.post("/{channel}/{title}/{body}/{key}")
async def send_by_path_and_param(
    channel: str, title: str = "", body: str = "", key: str = ""
):
    return serve(channel, title, body, key)


@app.post("/send")
async def send_by_post_json(request: PostRequest):
    return serve(request.channel, request.title, request.body, request.key)


@app.post("/sendForm")
async def send_by_post_form(
    channel: str = Form(),
    title: str = Form(),
    body: str = Form(),
    key: str = Form(default=""),
):
    if channel == "":
        return {"code": -1, "message": "channel cannot be empty"}
    return serve(channel, title, body, key)


def serve(channel: str, title: str = "", body: str = "", key: str = ""):
    env = get_env()
    if env.key != "" and key != env.key:
        return {"code": -1, "message": "key not authorized"}
    channels = channel.split("+")
    senders = []
    for chan in channels:
        if chan == "bark":
            message = BarkMessage(title, body)
            sender = Bark(message)
        elif chan == "wecom-webhook":
            message = WecomMessage(title, body)
            sender = WecomWebhook(message)
        elif chan == "wecom-app":
            message = WecomMessage(title, body)
            sender = WecomApp(message)
        elif chan == "pushdeer":
            message = PushDeerMessage(title, body)
            sender = PushDeer(message)
        elif chan == "pushover":
            message = PushoverMessage(title, body)
            sender = Pushover(message)
        elif chan == "chanify":
            message = ChanifyMessage(title, body)
            sender = Chanify(message)
        elif chan == "email":
            message = EmailMessage(title, body)
            sender = Email(message)
        else:
            return {"code": 2, "message": f"{chan} is not supported"}
        senders.append(sender)

    errors = {}
    for sender in senders:
        rs, msg = sender.send()
        if not rs:
            errors[sender.get_name()] = msg

    if len(errors) == 0:
        return {"code": 0, "message": "success"}
    err_msg = ""
    for err in errors.items():
        err_msg += f"{err[0]} return: {err[1]}."
    return {"code": 1, "message": err_msg}


@app.exception_handler(ParamException)
@app.exception_handler(WecomException)
async def exception_handler(request, exc):
    return JSONResponse({"code": 3, "message": exc.message})
