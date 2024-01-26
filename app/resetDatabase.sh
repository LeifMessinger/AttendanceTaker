#!/bin/bash

alias python='python3'
function python {
        python3 $@
}

if [ -f "./manage.py" ] ; then	#Make sure we're in the right folder
	APP_NAME="AttendanceTaker"

	rm ./db.sqlite3 #Remove the whole database

	git rm -rf ./$APP_NAME/migrations #Remove all migrations in case they are stored on git too
	rm -rf ./$APP_NAME/migrations	#Remove all migrations

	mkdir ./$APP_NAME/migrations
	touch ./$APP_NAME/migrations/__init__.py

	python manage.py migrate "$APP_NAME" zero --fake

	python manage.py makemigrations "$APP_NAME"

	python manage.py migrate "$APP_NAME" --fake-initial #Init the whole database

	python manage.py migrate #This might migrate the Website database a bunch of times, so maybe I'll have to remove those migrations too

	./createSuperUser.sh
else
	echo "We aren't in the app folder."
fi
