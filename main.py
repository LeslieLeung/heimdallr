from fastapi import FastAPI

from channel import Bark
from env import Env

env = Env().get_env()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/{method}/{}")
async def send(method: str):
    if method == "bark":
        channel = Bark
    else:
        return {"code": 1, "msg": "channel not implemented yet!"}

    pass
