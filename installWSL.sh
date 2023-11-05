sudo apt-get install python3
sudo apt-get install python-is-python3
#probably reboot here
pushd /tmp
sudo apt-get install wget
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
popd

cd ./app
pip3 install -r requirements.txt

sudo pip3 install pyOpenSSL --upgrade
sudo pip3 install cryptography --upgrade
