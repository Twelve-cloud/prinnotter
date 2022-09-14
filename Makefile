start: docker-compose.yaml
	sudo docker-compose build
	sudo docker-compose up

test: docker-compose.yaml
	sudo docker-compose exec web poetry run pytest
