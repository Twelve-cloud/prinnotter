FROM python:3.9.13-alpine3.16
LABEL maintainer="ilya.savin@innowise-group.com"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add bash postgresql-dev gcc python3-dev musl-dev poetry

WORKDIR /code
COPY pyproject.toml /code
RUN poetry config virtualenvs.in-project true
RUN poetry install

COPY . /code
RUN chmod +x django-entrypoint.sh && chmod +x celery-entrypoint.sh
