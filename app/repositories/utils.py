import functools
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import DBError

logger = logging.getLogger(__name__)


def handle_db_error(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as e:
            logger.error(f"Database error in {func.__name__}: {e}")
            raise DBError() from e

    return wrapper
