import json

from fastapi import APIRouter, Request

from heimdallr.api.base import serve_channels_async
from heimdallr.webhook.github_star import GithubStarWebhook

webhook_router = APIRouter(prefix="/webhook")


@webhook_router.post("/github/star/{key}")
async def github_star(key: str, req: Request):
    body = await req.body()
    webhook = GithubStarWebhook(json.loads(body))
    title, msg_body, jump_url = webhook.parse()
    return await serve_channels_async(key, title, msg_body, jump_url=jump_url)
