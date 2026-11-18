


import httpx

from app.config import THREADS_USER_ID, THREADS_ACCESS_TOKEN
from app.platforms.base import BasePlatform
from app.schemas import PostingRequest, PlatformResult


class ThreadsPlatform(BasePlatform):
    platform_name = "threads"

    async def publish(self, request: PostingRequest) -> PlatformResult:
        if not THREADS_USER_ID or not THREADS_ACCESS_TOKEN:
            return PlatformResult(
                platform=self.platform_name,
                success=False,
                error="Threads credentials are not configured.",
            )

        base_url = "https://graph.threads.net/v1.0"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:

                # Step 1: Create the text post container
                create_response = await client.post(
                    f"{base_url}/{THREADS_USER_ID}/threads",
                    data={
                        "media_type": "TEXT",
                        "text": request.message,
                        "access_token": THREADS_ACCESS_TOKEN,
                    },
                )

                create_data = create_response.json()

                if not create_response.is_success or not create_data.get("id"):
                    return PlatformResult(
                        platform=self.platform_name,
                        success=False,
                        error=create_data.get("error", {}).get(
                            "message",
                            "Threads container creation failed.",
                        ),
                    )

                # Step 2: Publish the container
                publish_response = await client.post(
                    f"{base_url}/{THREADS_USER_ID}/threads_publish",
                    data={
                        "creation_id": create_data["id"],
                        "access_token": THREADS_ACCESS_TOKEN,
                    },
                )

                publish_data = publish_response.json()

                if publish_response.is_success and publish_data.get("id"):
                    post_id = publish_data["id"]

                    # Step 3: Retrieve the published post permalink
                    permalink_response = await client.get(
                        f"{base_url}/{post_id}",
                        params={
                            "fields": "permalink",
                            "access_token": THREADS_ACCESS_TOKEN,
                        },
                    )

                    permalink_data = permalink_response.json()

                    published_url = (
                        permalink_data.get("permalink")
                        if permalink_response.is_success
                        else None
                    )

                    return PlatformResult(
                        platform=self.platform_name,
                        success=True,
                        post_id=post_id,
                        published_url=published_url,
                    )

                return PlatformResult(
                    platform=self.platform_name,
                    success=False,
                    error=publish_data.get("error", {}).get(
                        "message",
                        "Threads publishing failed.",
                    ),
                )

        except httpx.HTTPError as exc:
            return PlatformResult(
                platform=self.platform_name,
                success=False,
                error=f"Threads connection error: {type(exc).__name__}",
            )
