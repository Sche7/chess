setup:
	pip install -U pip setuptools
	pip install -r requirements.txt
	pip install -e .

play-chess:
	chess --c src/config.yml
