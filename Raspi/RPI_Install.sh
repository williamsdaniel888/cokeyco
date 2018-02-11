#!/bin/bash 

# Make Sure script is running as SUDO
if [[ $EUID > 0 ]]; then # we can compare directly with this syntax.
  echo "Please run as root/sudo"
  exit 1
fi


#Upgrade all packages
apt-get update && apt-get -y upgrade 
echo "Update Complete Successfully"

#Change Passowrd
yes "embeded" | passwd pi
echo "Password Changed Successfully"
#Enable SSH
if [ -e /var/log/regen_ssh_keys.log ] && ! grep -q "^finished" /var/log/regen_ssh_keys.log; then
whiptail --msgbox "Initial ssh key generation still running. Please wait and try again." 20 60 2
return 1
fi
update-rc.d ssh enable &&
invoke-rc.d ssh start &&
echo "SSH Server Enabled"




apt-get -y install mosquitto 
