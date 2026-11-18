
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from app.platforms.facebook import FacebookPlatform
from app.schemas import PostingRequest


def test_facebook_publish_success():
    async def run_test():
        request = PostingRequest(
            message="Testing Dxora Facebook integration",
            cta_url="https://example.com",
        )

        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {"id": "123_456"}

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response

        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_client)
        mock_context.__aexit__ = AsyncMock(return_value=None)

        with (
            patch(
                "app.platforms.facebook.FACEBOOK_PAGE_ID",
                "test_page_id",
            ),
            patch(
                "app.platforms.facebook.FACEBOOK_PAGE_ACCESS_TOKEN",
                "test_token",
            ),
            patch(
                "app.platforms.facebook.httpx.AsyncClient",
                return_value=mock_context,
            ),
        ):
            result = await FacebookPlatform().publish(request)

        assert result.success is True
        assert result.platform == "facebook"
        assert result.post_id == "123_456"
        assert result.published_url == "https://www.facebook.com/123_456"

    asyncio.run(run_test())
