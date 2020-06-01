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

# Disable ERTM otherwise XBOX one controller wont remain connected after BT pairing
echo "Disabling ERTM"
/bin/cat <<EOM >/etc/modprobe.d/bluetooth.conf
options bluetooth disable_ertm=1
EOM

apt-get update
apt-get -y upgrade
apt-get -y install expect bluez evtest python3-pip python3 python3-pyudev python3-evdev dkms raspberrypi-kernel-headers git

echo "Download xbox drivers"
git clone https://github.com/atar-axis/xpadneo.git
cd xpadneo && ./install.sh

cd /boot/pi-board || exit
pip3 install ds4drv pyyaml evdev

echo "Set up controller rules"
cp ./usb/50-ds4drv.rules /etc/udev/rules.d/50-ds4drv.rules
udevadm control --reload-rules
udevadm trigger

# Copy BT services
cp ./bluetooth/ps4-bt-controller.service /etc/systemd/system/ps4-bt-controller.service
cp ./bluetooth/standard-bt-controller.service /etc/systemd/system/standard-bt-controller.service
cp ./bluetooth/ps4-bt-controller.timer /etc/systemd/system/ps4-bt-controller.timer
cp ./key-mapper/pi-board-key-mapper.service /etc/systemd/system/pi-board-key-mapper.service
cp ./usb/isticktoit.service /etc/systemd/system/isticktoit.service

chmod 644 /etc/systemd/system/standard-bt-controller.service
chmod 644 /etc/systemd/system/standard-bt-controller.timer
chmod 644 /etc/systemd/system/pi-board-key-mapper.service
chmod 644 /etc/systemd/system/isticktoit.service

echo "register services"
systemctl enable isticktoit
systemctl enable pi-board-key-mapper

echo "Rebooting"
reboot
