.PHONY: run up up-build down down-v logs prod-up prod-up-build lint lint-fix format pre-commit
DC = docker compose

run:
	.venv/Scripts/uvicorn.exe app.main:app --reload

lint:
	python -m ruff check .

lint-fix:
	python -m ruff check --fix .

format:
	python -m ruff format .

pre-commit:
	python -m pre_commit run --all-files

test:
	python -m pytest

up:
	$(DC) up

prod-up:
	$(DC) -f docker-compose.yml -f docker-compose.prod.yml up

prod-up-build:
	$(DC) -f docker-compose.yml -f docker-compose.prod.yml up --build

up-build:
	$(DC) up --build

down:
	$(DC) down

down-v:
	$(DC) down -v

logs:
	$(DC) logs -f
