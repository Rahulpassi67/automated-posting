
import asyncio

from app.platforms.base import BasePlatform
from app.schemas import PostingRequest, PlatformResult


async def publish_safely(
    platform: BasePlatform,
    request: PostingRequest,
) -> PlatformResult:
    """Publish to one platform without affecting other platforms."""
    try:
        return await platform.publish(request)
    except Exception as exc:
        return PlatformResult(
            platform=platform.platform_name,
            success=False,
            error=f"Unexpected error: {type(exc).__name__}",
        )


async def publish_to_platforms(
    request: PostingRequest,
    platforms: list[BasePlatform],
) -> list[PlatformResult]:
    """Publish concurrently and isolate individual platform failures."""
    return await asyncio.gather(
        *(
            publish_safely(platform, request)
            for platform in platforms
        )
    )
