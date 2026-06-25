FROM python:3.13-slim AS base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /code
COPY pyproject.toml uv.lock ./

FROM base AS dev
RUN uv sync --frozen
COPY ./app ./app
COPY ./tests ./tests

FROM base AS prod
RUN uv sync --frozen --no-dev
COPY ./app ./app
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
