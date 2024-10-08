install:
	poetry install
	poetry run pre-commit install

dev:
	poetry run fastapi dev car_wash/main.py

compose-dev:
	docker compose up -d --remove-orphans
	make dev

lint:
	poetry run ruff check

lint_fix:
	poetry run ruff check --fix

format:
	poetry run ruff format

start_db:
	docker compose start db

enter_db:
	docker compose exec -it db psql -U pguser -d pgdb psql

# make migrations is not working for some reason
# make: 'migrations' is up to date.
db_migrations:
	poetry run alembic revision --autogenerate

migrate:
	poetry run alembic upgrade head
