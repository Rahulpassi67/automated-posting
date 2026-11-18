
from abc import ABC, abstractmethod

from app.schemas import PostingRequest, PlatformResult


class BasePlatform(ABC):
    """Common interface for all social media integrations."""

    platform_name: str = "base"

    @abstractmethod
    async def publish(
        self,
        request: PostingRequest
    ) -> PlatformResult:
        """Publish content to the connected platform."""
        raise NotImplementedError
