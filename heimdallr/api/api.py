from fastapi import APIRouter

from heimdallr.api import competable, push, webhook

router = APIRouter()
router.include_router(webhook.webhook_router)
router.include_router(competable.competable_router)
router.include_router(push.push_router)
