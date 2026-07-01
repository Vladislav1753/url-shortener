import logging
from typing import Annotated
from http import HTTPStatus
from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from app.schemas.link import LinkCreate, LinkRead
from app.services.link import LinkService

from app.api.dependencies import get_link_service


logger = logging.getLogger(__name__)

link_router = APIRouter(prefix="/links", tags=["links"])


@link_router.post("/", status_code=HTTPStatus.CREATED, response_model=LinkRead)
async def create(
    link: LinkCreate,
    service: Annotated[LinkService, Depends(get_link_service)],
) -> LinkRead:
    return await service.create_link(link=link)


@link_router.get(
    "/{code}",
)
async def get_link(
    code: str,
    service: Annotated[LinkService, Depends(get_link_service)],
) -> RedirectResponse:
    link = await service.get_and_count(code=code)
    return RedirectResponse(
        url=link.original_url,
        status_code=HTTPStatus.FOUND,
    )
