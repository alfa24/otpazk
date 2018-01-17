#!/bin/sh
#python /app/manage.py collectstatic --noinput
/usr/local/bin/gunicorn otpazk.wsgi -w 4 -b 0.0.0.0:8000 --chdir=/app
