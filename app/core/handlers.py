import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from http import HTTPStatus

from app.core.exceptions import (
    DBError,
    CodeAlreadyExistsError,
    CodeNotFoundError,
    CouldNotGenerateCodeError,
)

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(DBError)
    async def db_exception_handler(request: Request, exc: DBError):
        logger.error(f"Database error: {exc.message}")

        return JSONResponse(
            {"detail": "Error with the database"},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(CodeNotFoundError)
    async def code_not_found_handler(request: Request, exc: CodeNotFoundError):
        logger.error(str(exc))
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"detail": exc.message},
        )

    @app.exception_handler(CodeAlreadyExistsError)
    async def code_already_exists_handler(
        request: Request, exc: CodeAlreadyExistsError
    ):
        logger.error(str(exc))

        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={"detail": exc.message},
        )

    @app.exception_handler(CouldNotGenerateCodeError)
    async def code_generation_handler(request: Request, exc: CouldNotGenerateCodeError):
        logger.warning(f"Code generation error: {exc.message}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"detail": exc.message},
        )
