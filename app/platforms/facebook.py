

import httpx

from app.config import FACEBOOK_PAGE_ID, FACEBOOK_PAGE_ACCESS_TOKEN
from app.platforms.base import BasePlatform
from app.schemas import PostingRequest, PlatformResult


class FacebookPlatform(BasePlatform):
    platform_name = "facebook"

    async def publish(self, request: PostingRequest) -> PlatformResult:
        # Check whether Facebook credentials are configured
        if not FACEBOOK_PAGE_ID or not FACEBOOK_PAGE_ACCESS_TOKEN:
            return PlatformResult(
                platform=self.platform_name,
                success=False,
                error="Facebook Page credentials are not configured.",
            )

        # Facebook Graph API endpoint
        url = (
            f"https://graph.facebook.com/v27.0/"
            f"{FACEBOOK_PAGE_ID}/feed"
        )

        # Post content
        payload = {
            "message": request.message,
            "access_token": FACEBOOK_PAGE_ACCESS_TOKEN,
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, data=payload)

            data = response.json()

            # Successful publishing
            if response.is_success and data.get("id"):
                post_id = data["id"]

                return PlatformResult(
                    platform=self.platform_name,
                    success=True,
                    post_id=post_id,
                    published_url=f"https://www.facebook.com/{post_id}",
                )

            # Facebook API error
            return PlatformResult(
                platform=self.platform_name,
                success=False,
                error=data.get("error", {}).get(
                    "message",
                    "Facebook publishing failed.",
                ),
            )

        except httpx.HTTPError as exc:
            return PlatformResult(
                platform=self.platform_name,
                success=False,
                error=f"Facebook connection error: {type(exc).__name__}",
            )
