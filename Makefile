setup-dev:
	poetry install --with dev
	pre-commit install

play-chess:
	poetry run chess --c src/config.yml

format:
	poetry run ruff format

lint:
	poetry run ruff check . --fix

testing:
	poetry run pytest .
