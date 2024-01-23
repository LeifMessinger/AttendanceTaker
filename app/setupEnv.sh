alias python='python3'
function python {
	python3 $@
}
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --break-system-packages
exit
