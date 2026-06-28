from sqlalchemy import update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from app.core.exceptions import CodeAlreadyExistsError, DBError
from app.models.link import Link
from app.repositories.utils import handle_db_error


class LinkRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def create(self, link: Link) -> Link:
        try:
            self.session.add(link)
            await self.session.flush()
            await self.session.refresh(link)
        except IntegrityError:
            raise CodeAlreadyExistsError(code=link.code)
        except SQLAlchemyError as e:
            raise DBError() from e

        return link

    @handle_db_error
    async def get_by_code(self, code: str) -> Link | None:
        result = await self.session.execute(select(Link).where(Link.code == code))
        return result.scalar_one_or_none()

    @handle_db_error
    async def increment_clicks(self, code: str) -> None:
        await self.session.execute(
            update(Link)
            .where(Link.code == code)
            .values(clicks=Link.clicks + 1)
            .execution_options(synchronize_session=False)
        )
