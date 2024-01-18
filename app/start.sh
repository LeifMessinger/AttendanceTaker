./setupEnv.sh
source venv/bin/activate
./migrate.sh
python3 ./manage.py collectstatic --noinput && python3 ./manage.py runserver 0.0.0.0:8000
exit	#Hopefully this exits the env
