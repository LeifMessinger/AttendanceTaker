#!/bin/bash

APP_NAME="AttendanceTaker"

python manage.py migrate "$APP_NAME" zero --fake

python manage.py makemigrations "$APP_NAME"

python manage.py migrate "$APP_NAME" --fake-initial
