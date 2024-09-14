from fastapi import APIRouter, Form, Query, Request
from fastapi.responses import JSONResponse

from heimdallr.api.base import serve_channels_async

competable_router = APIRouter(prefix="/competable")


@competable_router.post("/pushdeer/message/push")
async def pushdeer_message_push(request: Request):
    content_type = request.headers.get("Content-Type", "")

    if "application/json" in content_type:
        data = await request.json()
        text = data.get("text")
        desp = data.get("desp")
        pushkey = data.get("pushkey")
        type = data.get("type", "text")
    elif "application/x-www-form-urlencoded" in content_type:
        form_data = await request.form()
        text = form_data.get("text")
        desp = form_data.get("desp")
        pushkey = form_data.get("pushkey")
        type = form_data.get("type", "text")
    else:
        return JSONResponse(status_code=415, content={"error": "Unsupported Media Type"})

    if not all([text, desp, pushkey]):
        return JSONResponse(status_code=400, content={"error": "Missing required fields"})

    try:
        await serve_channels_async(str(pushkey), str(text), str(desp))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return {
        "code": 0,
        "content": {
            "result": [
                '{"counts":1,"logs":[],"success":"ok"}',
            ]
        },
    }


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
