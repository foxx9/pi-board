#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root by typing sudo su"
  exit
fi

cd /boot/pi-board || exit

#usb driver creation script
chmod 755 ./bluetooth/*.sh
chmod 755 ./usb/*.sh

#Setup needed modules
echo "Updating modules"
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
echo "libcomposite" | sudo tee -a /etc/modules

#Create service to make it start as soon as possible when device is powered on
echo "Creating USB service"
cp ./usb/isticktoit.service /etc/systemd/system/isticktoit.service
chmod 644 /etc/systemd/system/isticktoit.service
systemctl enable isticktoit

# Disable ERTM otherwise XBOX one controller wont remain connected after BT pairing
echo "Disabling ERTM"
/bin/cat <<EOM >/etc/modprobe.d/bluetooth.conf
options bluetooth disable_ertm=1
EOM

apt-get update
apt-get -y upgrade
apt-get -y install expect bluez evtest python3-pip python3 python3-pyudev python3-evdev dkms raspberrypi-kernel-headers git

git clone https://github.com/atar-axis/xpadneo.git
cd xpadneo && ./install.sh

echo "Download xbox drivers"
cd /boot/pi-board || exit
pip3 install ds4drv pyyaml

echo "Set up controller rules"
cp ./usb/50-ds4drv.rules /etc/udev/rules.d/50-ds4drv.rules
udevadm control --reload-rules
udevadm trigger

# Cronjob to reconnect the BT controller if connection lost
echo "Creation crontab"
crontab -l >mycron
echo "* * * * * /bin/bash /boot/pi-board/bluetooth/connect-controller.sh" >>mycron
#install new cron file
crontab mycron
rm mycron

echo "Rebooting"
reboot
