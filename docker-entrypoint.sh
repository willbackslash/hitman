#!/bin/sh

set -xe
exec uwsgi --ini uwsgi.ini "$@"
