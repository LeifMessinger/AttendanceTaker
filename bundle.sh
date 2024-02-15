sudo systemctl start docker
sudo docker compose build
#Get the last created image
IMAGE_ID=`sudo docker images | gawk '{print $3}' | head -n 2 | tail -n 1`
echo $IMAGE_ID
wget https://github.com/rzane/docker2exe/releases/download/v0.2.1/docker2exe-linux-amd64 -O docker2exe
chmod 755 docker2exe
./docker2exe --name AttendanceTaker --image $IMAGE_ID
#This will put the exe in the dist folder

#A little cleanup. This might stop the server if you're running it while doing this.
sudo docker image rm $IMAGE_ID

#This will work on any computer with docker, but that probably exclude the school computers. :(
#If you have root access, you can use this build of docker
#https://download.docker.com/win/static/stable/x86_64/docker-24.0.7.zip

#Just download it, unzip it to a folder, and add it to the path in powershell by doing
echo 'Do this in powershell before running the exe:'
echo '$env:Path += ";D:\Whatever\Your\Path\Is\docker"'
#Then run the dockerd and then the exe that this generates
