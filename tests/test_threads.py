

import asyncio
from unittest.mock import patch

from app.platforms.threads import ThreadsPlatform
from app.schemas import PostingRequest


class FakeResponse:
    def __init__(self, data):
        self.data = data
        self.is_success = True

    def json(self):
        return self.data


class FakeAsyncClient:
    def __init__(self, *args, **kwargs):
        self.responses = [
            FakeResponse({"id": "container123"}),
            FakeResponse({"id": "thread456"}),
        ]

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def post(self, *args, **kwargs):
        return self.responses.pop(0)

    async def get(self, *args, **kwargs):
        return FakeResponse({
            "permalink": (
                "https://www.threads.net/@dxora.official/post/test123"
            )
        })


def test_threads_publish_success():
    async def run_test():
        with (
            patch(
                "app.platforms.threads.THREADS_USER_ID",
                "test_user_id",
            ),
            patch(
                "app.platforms.threads.THREADS_ACCESS_TOKEN",
                "test_token",
            ),
            patch(
                "app.platforms.threads.httpx.AsyncClient",
                FakeAsyncClient,
            ),
        ):
            request = PostingRequest(
                message="Testing Dxora",
                cta_url="https://example.com",
            )

            result = await ThreadsPlatform().publish(request)

            assert result.success is True
            assert result.post_id == "thread456"
            assert result.platform == "threads"
            assert result.published_url == (
                "https://www.threads.net/@dxora.official/post/test123"
            )

    asyncio.run(run_test())
