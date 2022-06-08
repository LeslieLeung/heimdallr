from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from channel import (Bark, BarkMessage, PushDeer, PushDeerMessage, Pushover,
                     PushoverMessage, WecomApp, WecomMessage, WecomWebhook)
from env import get_env
from exception import ParamException, WecomException

app = FastAPI()


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
    if channel == "bark":
        message = BarkMessage(title, body)
        channel = Bark(message)
    elif channel == "wecom-webhook":
        message = WecomMessage(title, body)
        channel = WecomWebhook(message)
    elif channel == "wecom-app":
        message = WecomMessage(title, body)
        channel = WecomApp(message)
    elif channel == "pushdeer":
        message = PushDeerMessage(title, body)
        channel = PushDeer(message)
    elif channel == "pushover":
        message = PushoverMessage(title, body)
        channel = Pushover(message)
    else:
        return {"code": 2, "message": f"{channel} is not supported"}
    rs, msg = channel.send()
    if rs:
        return {"code": 0, "message": msg}
    return {"code": 1, "message": f"{channel} return {msg}"}


@app.exception_handler(ParamException)
@app.exception_handler(WecomException)
async def exception_handler(request, exc):
    return JSONResponse({"code": 3, "message": exc.message})
