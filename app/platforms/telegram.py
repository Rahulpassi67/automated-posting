

import os
import asyncio
from datetime import datetime, timezone
import py_compile

import requests

from app.platforms.base import BasePlatform
from app.schemas import PostingRequest, PlatformResult


class TelegramPlatform(BasePlatform):
    """Telegram social media integration."""

    platform_name = "telegram"

    async def publish(
        self,
        request: PostingRequest
    ) -> PlatformResult:

        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")

        # Check Telegram credentials
        if not token or not chat_id:
            return PlatformResult(
                platform="telegram",
                success=False,
                error="Telegram credentials are missing."
            )

        # Prepare message with CTA URL
        message = f"{request.message}\n\n{request.cta_url}"

        try:
            def send_message():
                url = (
                    f"https://api.telegram.org/"
                    f"bot{token}/sendMessage"
                )

                response = requests.post(
                    url,
                    json={
                        "chat_id": chat_id,
                        "text": message,
                    },
                    timeout=20,
                )

                response.raise_for_status()
                data = response.json()

                if not data.get("ok"):
                    raise RuntimeError(
                        data.get(
                            "description",
                            "Telegram API error"
                        )
                    )

                return data["result"]

            # Run synchronous API request asynchronously
            result = await asyncio.to_thread(send_message)

            message_id = result["message_id"]

            # Telegram publication timestamp
            published_at = datetime.fromtimestamp(
                result["date"],
                tz=timezone.utc
            )

            # Public URL is available for public channels/groups
            chat = result.get("chat", {})
            username = chat.get("username")

            published_url = None

            if username:
                published_url = (
                    f"https://t.me/{username}/{message_id}"
                )

            return PlatformResult(
                platform="telegram",
                success=True,
                post_id=str(message_id),
                published_url=published_url,
                published_at=published_at
            )

        except Exception as exc:
            return PlatformResult(
                platform="telegram",
                success=False,
                error=str(exc)
            )
