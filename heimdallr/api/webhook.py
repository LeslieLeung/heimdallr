import json

from fastapi import APIRouter, Request

from heimdallr.api.api import serve
from heimdallr.webhook.github_star import GithubStarWebhook

webhook_router = APIRouter()


@webhook_router.post("/github/star/{channel}")
async def github_star(channel: str, req: Request):
    body = await req.body()
    webhook = GithubStarWebhook(json.loads(body))
    title, msg_body, jump_url = webhook.parse()
    return serve(channel, title, msg_body, jump_url=jump_url)
