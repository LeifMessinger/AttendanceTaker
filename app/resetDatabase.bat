:: Have to be in the python venv

@echo on

if exist "manage.py" (
    del /f db.sqlite3
    
    git rm -r ./AttendanceTaker/migrations :: This might error, but who cares
    
    python manage.py migrate "AttendanceTaker" zero --fake
    
    python manage.py makemigrations "AttendanceTaker"
    
    python manage.py migrate "AttendanceTaker" --fake-initial
    
    python manage.py migrate
    
    call createSuperUser.bat
) else (
    echo We aren't in the app folder.
)