#!/bin/sh
python manage.py collectstatic --no-input

set -xe
exec uwsgi --ini uwsgi.ini "$@"
