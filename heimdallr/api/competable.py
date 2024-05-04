from fastapi import APIRouter, Form, Query

from heimdallr.api.base import serve_channels_async

competable_router = APIRouter(prefix="/competable")


@competable_router.get("/message-pusher/push")
async def message_pusher_get(
    title: str = Query(...),
    description: str = Query(...),
    token: str = Query(...),
):
    return await serve_channels_async(token, title, description)


@competable_router.post("/message-pusher/push")
async def message_pusher_post(
    title: str = Form(...),
    description: str = Form(...),
    token: str = Form(...),
):
    return await serve_channels_async(token, title, description)
