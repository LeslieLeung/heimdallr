import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from env import is_debug
from heimdallr.api.api import router
from heimdallr.exception import ParamException, WecomException

app = FastAPI()

if is_debug():
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.ERROR)

app.include_router(router)


@app.exception_handler(ParamException)
@app.exception_handler(WecomException)
async def exception_handler(request, exc):
    return JSONResponse({"code": 3, "message": exc.message})
