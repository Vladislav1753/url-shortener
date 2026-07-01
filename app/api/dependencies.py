from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.repositories.link import LinkRepository
from app.services.link import LinkService


def get_link_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> LinkRepository:
    return LinkRepository(
        session=session,
    )


def get_link_service(
    repo: Annotated[LinkRepository, Depends(get_link_repo)],
) -> LinkService:
    return LinkService(
        repo=repo,
    )
