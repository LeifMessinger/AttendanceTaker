#!/bin/bash -x

sudo apt-get install python3
sudo apt-get install python-is-python3
#probably reboot here
pushd /tmp
sudo apt-get install wget
sudo apt-get install docker
sudo apt-get install docker-compose
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
popd

pushd ./app
pip3 install -r requirements.txt

sudo pip3 install pyOpenSSL --upgrade
sudo pip3 install cryptography --upgrade

git submodule update --init --recursive

./resetDatabase.sh
popd
