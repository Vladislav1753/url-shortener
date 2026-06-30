import pytest

from app.core.exceptions import CodeAlreadyExistsError
from tests.utils import make_link


async def test_create_link(repo):
    link_data = make_link()
    link = await repo.create(link_data)

    assert link.id is not None
    assert link.code == link_data.code
    assert link.original_url == link_data.original_url
    assert link.clicks == 0


async def test_get_link(repo, created_link):
    link = await repo.get_by_code(created_link.code)

    assert link is not None
    assert link.code == created_link.code
    assert link.original_url == created_link.original_url
    assert link.clicks == 0


async def test_increment_clicks(repo, session, created_link):
    await repo.increment_clicks(created_link.code)
    await session.refresh(created_link)

    assert created_link.clicks == 1


async def test_code_exists_error(repo, created_link):
    link = await repo.get_by_code(created_link.code)

    link_data = make_link(code=link.code)
    with pytest.raises(CodeAlreadyExistsError) as exc_info:
        await repo.create(link_data)

    assert exc_info.value.code == created_link.code
