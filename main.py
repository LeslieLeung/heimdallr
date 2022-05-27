from fastapi import FastAPI

from channel import Bark, BarkMessage

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/bark/{title}/{body}")
async def send_bark(title: str, body: str):
    message = BarkMessage(title, body)
    bark = Bark(message)
    rs, msg = bark.send()
    if rs:
        return {"code": 0, "message": msg}
    return {"code": 1, "message": f"bark return {msg}"}
