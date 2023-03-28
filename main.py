import json
import logging

from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from env import get_env, is_debug
from heimdallr.channel import (Bark, BarkMessage, Chanify, ChanifyMessage,
                               Email, EmailMessage, PushDeer, PushDeerMessage,
                               Pushover, PushoverMessage, WecomApp,
                               WecomMessage, WecomWebhook)
from heimdallr.exception import ParamException, WecomException
from heimdallr.webhook.github_star import GithubStarWebhook

app = FastAPI()

if is_debug():
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.ERROR)


class PostRequest(BaseModel):
    channel: str = ""
    title: str = ""
    body: str = ""
    key: str = ""
    msg_type: str = "text"


@app.post("/github/star/{channel}")
async def github_star(channel: str, req: Request):
    body = await req.body()
    webhook = GithubStarWebhook(json.loads(body))
    title, body, jump_url = webhook.parse()
    return serve(channel, title, body, jump_url=jump_url)


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


@app.post("/echo/{channel}")
async def echo(channel: str, request: Request):
    title = f"FROM [{request.url}]"
    body = await request.body()
    return serve(channel, title, body.decode("utf-8"))


@app.post("/wecom-app")
@app.post("/wecom-webhook")
async def send_wecom(request: Request, req: PostRequest):
    message = WecomMessage(req.title, req.body, req.msg_type)
    match request.url.path:
        case "/wecom-app":
            sender = WecomApp(message)
        case "/wecom-webhook":
            sender = WecomWebhook(message)
        case _:
            return {
                "code": 2,
                "message": f"channel {request.url.path[1:]} not supported",
            }
    rs, msg = sender.send()
    if not rs:
        raise WecomException(msg)
    return {"code": 0, "message": "success"}


def serve(channel: str, title: str = "", body: str = "", key: str = "", jump_url: str = ""):
    env = get_env()
    if env.key != "" and key != env.key:
        return {"code": -1, "message": "key not authorized"}
    channels = channel.split("+")
    senders = []
    for chan in channels:
        match chan:
            case "bark":
                message = BarkMessage(title, body, jump_url)
                sender = Bark(message)
            case "wecom-webhook":
                message = WecomMessage(title, body)
                sender = WecomWebhook(message)
            case "wecom-app":
                message = WecomMessage(title, body)
                sender = WecomApp(message)
            case "pushdeer":
                message = PushDeerMessage(title, body)
                sender = PushDeer(message)
            case "pushover":
                message = PushoverMessage(title, body)
                sender = Pushover(message)
            case "chanify":
                message = ChanifyMessage(title, body)
                sender = Chanify(message)
            case "email":
                message = EmailMessage(title, body)
                sender = Email(message)
            case _:
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
