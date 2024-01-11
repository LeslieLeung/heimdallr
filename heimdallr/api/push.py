from fastapi import APIRouter, Form, Request
from pydantic import BaseModel

from heimdallr.api.base import serve
from heimdallr.channel import Channel, WecomApp, WecomMessage, WecomWebhook
from heimdallr.exception import WecomException

push_router = APIRouter()


class PostRequest(BaseModel):
    channel: str = ""
    title: str = ""
    body: str = ""
    key: str = ""
    msg_type: str = "text"


@push_router.get("/{channel}")
@push_router.get("/{channel}/{title}/{body}")
@push_router.post("/{channel}/{title}/{body}")
@push_router.get("/{channel}/{title}/{body}/{key}")
@push_router.post("/{channel}/{title}/{body}/{key}")
async def send_by_path_and_param(
    channel: str, title: str = "", body: str = "", key: str = ""
):
    return serve(channel, title, body, key)


@push_router.post("/send")
async def send_by_post_json(request: PostRequest):
    return serve(request.channel, request.title, request.body, request.key)


@push_router.post("/sendForm")
async def send_by_post_form(
    channel: str = Form(),
    title: str = Form(),
    body: str = Form(),
    key: str = Form(default=""),
):
    if channel == "":
        return {"code": -1, "message": "channel cannot be empty"}
    return serve(channel, title, body, key)


@push_router.post("/echo/{channel}")
async def echo(channel: str, request: Request):
    title = f"FROM [{request.url}]"
    body = await request.body()
    return serve(channel, title, body.decode("utf-8"))


@push_router.post("/wecom-app")
@push_router.post("/wecom-webhook")
async def send_wecom(request: Request, req: PostRequest):
    message = WecomMessage(req.title, req.body, req.msg_type)
    sender: Channel
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
