from fastapi import FastAPI
from fastapi.responses import JSONResponse

from channel import Bark, BarkMessage, WecomApp, WecomMessage, WecomWebhook
from env import get_env
from exception import ParamException, WecomException

app = FastAPI()


@app.get("/{channel}")
@app.get("/{channel}/{title}/{body}")
@app.get("/{channel}/{title}/{body}/{key}")
async def send(channel: str, title: str = "", body: str = "", key: str = ""):
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
