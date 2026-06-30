import logging

from app.core.exceptions import (
    DBError,
    CodeAlreadyExistsError,
    CouldNotGenerateCodeError,
    CodeNotFoundError,
)
from app.models.link import Link
from app.repositories.link import LinkRepository
from app.schemas.link import LinkCreate, LinkRead
from app.utils import shortcode

logger = logging.getLogger(__name__)

MAX_CODE_ATTEMPTS = 5


class LinkService:
    def __init__(self, repo: LinkRepository):
        self.repo = repo

    async def create_link(self, link: LinkCreate) -> LinkRead:
        for _ in range(MAX_CODE_ATTEMPTS):
            new_link = Link(
                original_url=str(link.original_url),
                code=shortcode.generate(),
            )
            try:
                created_link = await self.repo.create(new_link)
                await self.repo.commit()
            except CodeAlreadyExistsError:
                await self.repo.rollback()
                continue
            except DBError:
                await self.repo.rollback()
                raise

            logger.info(f"New link created: {created_link.code}")
            return LinkRead.model_validate(created_link)

        raise CouldNotGenerateCodeError()

    async def get_and_count(self, code: str) -> LinkRead:
        try:
            link = await self.repo.get_by_code(code)
            if not link:
                raise CodeNotFoundError(code)
            await self.repo.increment_clicks(code)
            await self.repo.commit()
        except DBError:
            await self.repo.rollback()
            raise

        logger.info(f"Link found: {link.code}")
        return LinkRead.model_validate(link)
