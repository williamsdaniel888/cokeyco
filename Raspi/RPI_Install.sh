#!/bin/bash 

# Make Sure script is running as SUDO
if [[ $EUID > 0 ]]; then # we can compare directly with this syntax.
  echo "Please run as root/sudo"
  exit 1
fi


#Upgrade all packages
echo "Starting Package Update"
apt-get update && apt-get -y upgrade 
echo "Update Complete Successfully"

#Change Passowrd
yes "embeded" | passwd pi
echo "Password Changed Successfully"
#Enable SSH
while [ -e /var/log/regen_ssh_keys.log ] && ! grep -q "^finished" /var/log/regen_ssh_keys.log;
do
echo "Initial ssh key generation still running. Trying Again in 5 seconds"
sleep 5
fi
update-rc.d ssh enable &&
invoke-rc.d ssh start &&
echo "SSH Server Enabled"
sudo apt-get -y install git
# wget "https://raw.githubusercontent.com/williamsdaniel888/cokeyco/piers/Raspi/master.py" -O master.py
# wget "https://raw.githubusercontent.com/williamsdaniel888/cokeyco/piers/Raspi/mqttThread.py" -O mqttThread.py
# wget "https://github.com/williamsdaniel888/cokeyco/blob/piers/Raspi/music.py" -O music.py

wget ""



# Install and auto start mosquitto
apt-get -y install mosquitto 
