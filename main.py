import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from heimdallr.api.api import router
from heimdallr.exception import ParamException, WecomException

app = FastAPI()

logging.basicConfig(level=logging.INFO)

app.include_router(router)


@app.exception_handler(ParamException)
@app.exception_handler(WecomException)
async def exception_handler(request, exc):
    return JSONResponse({"code": 3, "message": exc.message})
