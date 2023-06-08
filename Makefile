setup:
	poetry shell
	poetry install

play-chess:
	poetry run chess --c src/config.yml
