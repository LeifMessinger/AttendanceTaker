#!/bin/bash

if [ -f "./manage.py" ] ; then	#Make sure we're in the right folder
	APP_NAME="AttendanceTaker"

	rm ./db.sqlite3 #Remove the whole database

	git rm -rf ./$APP_NAME/migrations #Remove all migrations

	python manage.py migrate "$APP_NAME" zero --fake

	python manage.py makemigrations "$APP_NAME"

	python manage.py migrate "$APP_NAME" --fake-initial #Init the whole database

	python manage.py migrate #This might migrate the Website database a bunch of times, so maybe I'll have to remove those migrations too

	./createSuperUser.sh
else
	echo "We aren't in the app folder."
fi
