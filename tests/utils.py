from datetime import datetime, timezone

from app.models.link import Link
from app.utils import shortcode


def make_link(url: str = "https://www.example.com", code: str | None = None) -> Link:
    return Link(
        original_url=url,
        code=code or shortcode.generate(),
    )


def make_persisted_link(
    url: str = "https://www.example.com", code: str | None = None
) -> Link:
    return Link(
        id=1,
        code=code or shortcode.generate(),
        original_url=url,
        clicks=0,
        created_at=datetime.now(timezone.utc),
    )
