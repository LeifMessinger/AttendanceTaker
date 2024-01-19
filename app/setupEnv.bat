:: Has to be run on a windows computer with python3 (as python)
python -m venv venv
call ./venv/Scripts/activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt --break-system-packages
call ./venv/Scripts/deactivate.bat