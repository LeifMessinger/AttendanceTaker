:: Have to run inside app folder

if exist ".\venv\Scripts\activate.bat" (
	call .\venv\Scripts\activate.bat
	call .\migrate.bat	:: Literally the same as migrate.sh
	python .\manage.py collectstatic --noinput & python .\manage.py runserver 0.0.0.0:8000

	call .\venv\Scripts\deactivate.bat	#Hopefully this exits the env
) else (
    echo We aren't in the app folder.
    pwd
)