#!/bin/bash
alias python='python3'
function python {
        python3 $@
}
env DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --username=admin --email=admin@admin.com --noinput
