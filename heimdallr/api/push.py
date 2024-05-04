import logging

from fastapi import APIRouter, Form, Query
from pydantic import BaseModel, Field

from heimdallr.api.base import serve_channels_async

logger = logging.getLogger(__name__)

push_router = APIRouter()


@push_router.post("/push/form")
async def send_push_by_form(
    key: str = Form(...),
    title: str = Form(...),
    body: str = Form(...),
    msg_type: str = Form(default="text"),
    attach: str = Form(default="", description="base64 string, only support image"),
):
    return await serve_channels_async(key, title, body, msg_type=msg_type, attach=attach)


class PostRequest(BaseModel):
    key: str = ""
    title: str = ""
    body: str = ""
    msg_type: str = "text"
    attach: str = Field("", description="base64 string, only support image")


@push_router.post("/push")
async def send_push_by_json(request: PostRequest):
    return await serve_channels_async(
        request.key,
        request.title,
        request.body,
        msg_type=request.msg_type,
        attach=request.attach,
    )


@push_router.get("/{key}")
@push_router.post("/{key}")
@push_router.get("/{key}/{body}")
@push_router.post("/{key}/{body}")
@push_router.get("/{key}/{title}/{body}")
@push_router.post("/{key}/{title}/{body}")
async def send_push(
    key: str,
    title: str = "",
    body: str = "",
    msg_type: str = "",
    attach: str = Query("", description="base64 string, only support image"),
):
    return await serve_channels_async(key, title, body, msg_type=msg_type, attach=attach)
