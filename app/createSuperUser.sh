#!/bin/bash
alias python='python3'
function python {
        python3 $@
}
openssl rand -base64 12 > superUserPassword.txt
env DJANGO_SUPERUSER_PASSWORD=$(cat superUserPassword.txt) python manage.py createsuperuser --username=admin --email=admin@admin.com --noinput
