

import asyncio

from atproto import Client

from app.config import BLUESKY_HANDLE, BLUESKY_APP_PASSWORD
from app.platforms.base import BasePlatform
from app.schemas import PostingRequest, PlatformResult


class BlueskyPlatform(BasePlatform):
    """Bluesky social media integration."""

    platform_name = "bluesky"

    async def publish(
        self,
        request: PostingRequest,
    ) -> PlatformResult:

        if not BLUESKY_HANDLE or not BLUESKY_APP_PASSWORD:
            return PlatformResult(
                platform=self.platform_name,
                success=False,
                error="Bluesky credentials are missing.",
            )

        def publish_post():
            client = Client()

            client.login(
                BLUESKY_HANDLE,
                BLUESKY_APP_PASSWORD,
            )

            message = request.message.strip()

            if request.cta_url:
                message += f"\n\n{request.cta_url}"

            response = client.send_post(text=message)

            return response.uri

        try:
            post_uri = await asyncio.to_thread(publish_post)

            record_key = post_uri.rsplit("/", 1)[-1]

            handle = BLUESKY_HANDLE.lstrip("@")

            published_url = (
                f"https://bsky.app/profile/{handle}/post/{record_key}"
            )

            return PlatformResult(
                platform=self.platform_name,
                success=True,
                post_id=post_uri,
                published_url=published_url,
            )

        except Exception as exc:
            return PlatformResult(
                platform=self.platform_name,
                success=False,
                error=f"Bluesky publishing failed: {str(exc)}",
            )
