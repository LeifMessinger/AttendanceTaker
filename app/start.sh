alias python='python3'
function python {
        python3 $@
}
./setupEnv.sh
source venv/bin/activate
./migrate.sh
python ./manage.py collectstatic --noinput && python ./manage.py runserver 0.0.0.0:8000
exit	#Hopefully this exits the env
