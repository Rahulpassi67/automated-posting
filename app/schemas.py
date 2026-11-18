
from typing import Literal
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_validator,
)


# Supported social media platforms
PlatformName = Literal[
    "bluesky",
    "mastodon",
    "telegram",
    "facebook",
    "threads",
]


# Incoming posting request
class PostingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str = Field(
        ...,
        min_length=1,
        max_length=200,
    )

    cta_url: HttpUrl

    @field_validator("cta_url")
    @classmethod
    def validate_cta_hostname(cls, value: HttpUrl) -> HttpUrl:
        hostname = value.host

        if not hostname or "." not in hostname:
            raise ValueError("CTA URL must have a valid hostname")

        return value


# Result from an individual platform
class PlatformResult(BaseModel):
    platform: PlatformName
    success: bool
    post_id: str | None = None
    published_url: str | None = None
    published_at: datetime | None = None
    error: str | None = None


# Final posting response
class PostingResponse(BaseModel):
    results: list[PlatformResult]
