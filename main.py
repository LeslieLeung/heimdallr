import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from heimdallr.api.api import router
from heimdallr.config.config import get_config_str, is_debug, log_env_vars
from heimdallr.exception import ParamException, WecomException

if is_debug():
    logging.basicConfig(level=logging.DEBUG)
    log_env_vars()
else:
    logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(router)


@app.exception_handler(ParamException)
@app.exception_handler(WecomException)
async def exception_handler(request, exc):
    return JSONResponse({"code": 3, "message": exc.message})


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(get_config_str("PORT", "", "9000")),
        log_level="info",
        access_log=True,
    )
