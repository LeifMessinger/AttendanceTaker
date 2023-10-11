#!/bin/bash
env DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --username=admin --email=admin@admin.com --noinput
