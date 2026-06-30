from app.models.link import Link
from app.utils import shortcode


def make_link(url: str = "https://www.example.com", code: str | None = None) -> Link:
    return Link(
        original_url=url,
        code=code or shortcode.generate(),
    )
