#!/bin/bash

#This doesn't work if docker is in rootless mode
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl show --property=Environment docker
