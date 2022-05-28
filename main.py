from fastapi import FastAPI

from channel import Bark, BarkMessage, WecomApp, WecomMessage, WecomWebhook

app = FastAPI()


@app.get("/{channel}")
@app.get("/{channel}/{title}/{body}")
async def send(channel: str, title: str = "", body: str = ""):
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
