import pytest

from app.core.exceptions import (
    CodeAlreadyExistsError,
    CouldNotGenerateCodeError,
    DBError,
    CodeNotFoundError,
)
from app.schemas.link import LinkRead, LinkCreate
from tests.utils import make_persisted_link

url = "https://www.example.com"


async def test_create_link_happy_path(mock_repo, service):
    mock_repo.create.return_value = make_persisted_link(url)

    result = await service.create_link(LinkCreate(original_url=url))

    assert isinstance(result, LinkRead)
    assert result.original_url == url
    mock_repo.create.assert_awaited_once()
    mock_repo.commit.assert_awaited_once()


async def test_create_link_collisions_success(mock_repo, service):
    mock_repo.create.side_effect = [
        CodeAlreadyExistsError(code="dummy"),
        CodeAlreadyExistsError(code="dummy"),
        make_persisted_link(url),
    ]

    result = await service.create_link(LinkCreate(original_url=url))

    assert isinstance(result, LinkRead)
    assert result.original_url == url
    assert mock_repo.rollback.await_count == 2
    assert mock_repo.create.await_count == 3
    mock_repo.commit.assert_awaited_once()


async def test_create_link_collisions_failure(mock_repo, service):
    mock_repo.create.side_effect = CodeAlreadyExistsError(code="dummy")

    with pytest.raises(CouldNotGenerateCodeError):
        await service.create_link(LinkCreate(original_url=url))

    assert mock_repo.rollback.await_count == 5
    assert mock_repo.create.await_count == 5
    mock_repo.commit.assert_not_awaited()


async def test_create_link_db_error(mock_repo, service):
    mock_repo.create.side_effect = DBError

    with pytest.raises(DBError):
        await service.create_link(LinkCreate(original_url=url))

    assert mock_repo.rollback.await_count == 1
    assert mock_repo.create.await_count == 1
    mock_repo.commit.assert_not_awaited()


async def test_get_and_count(mock_repo, service):
    link = make_persisted_link(url)
    mock_repo.get_by_code.return_value = link

    result = await service.get_and_count(link.code)

    assert isinstance(result, LinkRead)
    assert result.original_url == url
    mock_repo.get_by_code.assert_awaited_once_with(link.code)
    mock_repo.increment_clicks.assert_awaited_once_with(link.code)
    mock_repo.commit.assert_awaited_once()


async def test_get_and_count_not_found(mock_repo, service):
    mock_repo.get_by_code.return_value = None
    with pytest.raises(CodeNotFoundError):
        await service.get_and_count(code="dummy")

    mock_repo.get_by_code.assert_awaited_once()
    mock_repo.increment_clicks.assert_not_awaited()
    mock_repo.commit.assert_not_awaited()
