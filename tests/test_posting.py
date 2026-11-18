

import asyncio

from app.main import publish_safely
from app.platforms.base import BasePlatform
from app.schemas import PostingRequest, PlatformResult


class MockPlatform(BasePlatform):
    def __init__(self, platform_name, should_fail=False):
        self.platform_name = platform_name
        self.should_fail = should_fail

    async def publish(self, request):
        if self.should_fail:
            raise RuntimeError("Simulated platform failure")

        return PlatformResult(
            platform=self.platform_name,
            success=True,
            post_id="mock-post-123"
        )


def test_platform_failure_isolated():
    request = PostingRequest(
        message="Testing Dxora",
        cta_url="https://example.com"
    )

    platforms = [
        MockPlatform("bluesky"),
        MockPlatform("telegram", should_fail=True),
        MockPlatform("mastodon")
    ]

    async def run_test():
        results = [
            await publish_safely(platform, request)
            for platform in platforms
        ]
        return results

    results = asyncio.run(run_test())

    assert results[0].success is True
    assert results[1].success is False
    assert results[2].success is True
