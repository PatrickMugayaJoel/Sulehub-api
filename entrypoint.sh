#!/bin/sh

python /code/manage.py migrate --no-input
python /code/manage.py collectstatic --no-input
python /code/manage.py createsuperuser --noinput

gunicorn core.wsgi:application --bind 0.0.0.0:8000
