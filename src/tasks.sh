#!/bin/bash

cd /opt/otpazk/src
/opt/otpazk/.venv/bin/python manage.py runtasks
/opt/otpazk/.venv/bin/python manage.py checktime
