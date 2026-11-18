

from fastapi import FastAPI

from app.config import APP_NAME, APP_ENV
from app.schemas import PostingRequest, PostingResponse
from app.platforms.bluesky import BlueskyPlatform
from app.platforms.telegram import TelegramPlatform
from app.platforms.mastodon import MastodonPlatform
from app.platforms.threads import ThreadsPlatform
from app.platforms.facebook import FacebookPlatform
from app.services.posting_service import (
    publish_to_platforms,
    publish_safely,
)

app = FastAPI(
    title=APP_NAME,
    description="Automated multi-platform posting API",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {APP_NAME}",
        "environment": APP_ENV,
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "application": APP_NAME,
    }


@app.post("/posting", response_model=PostingResponse)
async def create_post(request: PostingRequest):
    platforms = [
        BlueskyPlatform(),
        TelegramPlatform(),
        MastodonPlatform(),
        ThreadsPlatform(),
        FacebookPlatform(),

    ]

    results = await publish_to_platforms(request, platforms)

    return PostingResponse(results=results)
