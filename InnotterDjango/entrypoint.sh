#! /bin/bash
poetry run python manage.py migrate
poetry run python manage.py createsuperuser --noinput
poetry run python manage.py runserver 0.0.0.0:${PORT:-8000}
