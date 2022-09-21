test:
	cd InnotterDjango && poetry run pytest
	cd InnotterDjango && flake8 .

build: docker-compose.yml
	sudo docker compose build

deploy:
	sudo docker compose up
