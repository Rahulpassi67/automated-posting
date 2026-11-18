
import os
import asyncio
from datetime import datetime, timezone

import requests

from app.platforms.base import BasePlatform
from app.schemas import PostingRequest, PlatformResult


class MastodonPlatform(BasePlatform):
    platform_name = "mastodon"

    async def publish(self, request: PostingRequest) -> PlatformResult:
        base_url = os.getenv("MASTODON_BASE_URL")
        access_token = os.getenv("MASTODON_ACCESS_TOKEN")

        if not base_url or not access_token:
            return PlatformResult(
                platform="mastodon",
                success=False,
                error="Mastodon credentials are missing."
            )

        try:
            def publish_post():
                status_text = f"{request.message}\n{request.cta_url}"

                response = requests.post(
                    f"{base_url.rstrip('/')}/api/v1/statuses",
                    headers={
                        "Authorization": f"Bearer {access_token}"
                    },
                    data={
                        "status": status_text
                    },
                    timeout=30
                )

                response.raise_for_status()
                return response.json()

            result = await asyncio.to_thread(publish_post)

            return PlatformResult(
                platform="mastodon",
                success=True,
                post_id=str(result["id"]),
                published_url=result.get("url"),
                published_at=result.get("created_at") or datetime.now(timezone.utc),
                error=None
            )

        except requests.RequestException:
            return PlatformResult(
                platform="mastodon",
                success=False,
                error="Mastodon API request failed. Check the connection and credentials."
            )
        except Exception as exc:
            return PlatformResult(
                platform="mastodon",
                success=False,
                error=f"Unexpected error: {type(exc).__name__}"
            )
