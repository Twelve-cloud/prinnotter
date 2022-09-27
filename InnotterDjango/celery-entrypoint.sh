#! /bin/bash
set -o errexit
set -o nounset
poetry run celery -A InnotterDjango worker --loglevel=INFO
