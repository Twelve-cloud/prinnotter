#! /bin/bash
poetry run python manage.py makemigrations
poetry run python manage.py makemigrations user
poetry run python manage.py makemigrations blog
poetry run python manage.py migrate
poetry run python manage.py migrate user
poetry run python manage.py migrate blog
poetry run python manage.py createsuperuser --noinput
poetry run python manage.py runserver 0.0.0.0:8000
