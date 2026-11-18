

import os
import asyncio
from datetime import datetime, timezone

from atproto import Client

from app.platforms.base import BasePlatform
from app.schemas import PostingRequest, PlatformResult


class BlueskyPlatform(BasePlatform):
    """Bluesky social media integration."""

    platform_name: str = "bluesky"

    async def publish(
        self,
        request: PostingRequest
    ) -> PlatformResult:

        handle = os.getenv("BLUESKY_HANDLE")
        app_password = os.getenv("BLUESKY_APP_PASSWORD")

        if not handle or not app_password:
            return PlatformResult(
                platform="bluesky",
                success=False,
                error="Bluesky credentials are missing."
            )

        try:
            def publish_post():
                client = Client()
                client.login(handle, app_password)

                message = request.message

                if request.cta_url:
                    message += f"\n{request.cta_url}"

                response = client.send_post(text=message)

                return response.uri

            post_uri = await asyncio.to_thread(publish_post)

            record_key = post_uri.split("/")[-1]

            published_url = (
                f"https://bsky.app/profile/{handle}/post/{record_key}"
            )

            return PlatformResult(
                platform="bluesky",
                success=True,
                post_id=post_uri,
                published_url=published_url,
                published_at=datetime.now(timezone.utc)
            )

        except Exception as exc:
            return PlatformResult(
                platform="bluesky",
                success=False,
                error=str(exc)
            )
