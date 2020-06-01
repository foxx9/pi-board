# Pi-Board project for RG350


## SD card setup
Here are the instruction for a fresh install of the raspbian image.
If you already have an accessible Raspberry PI ZERO W via ssh you can skip this part

1. Download and unzip this project sources
1. Flash the most recent image of Raspbian (I used the lite version : 2020-05-27-raspios-buster-lite-armhf at this time using https://www.raspberrypi.org/downloads/) 
2. Rename  `wpa_supplicant_example.conf` to `wpa_supplicant.conf` and put your WIFI settings ( you could setup a fixed IP in your router settings, so it will be easier to SSH later )
3. Copy `ssh` and `wpa_supplicant.conf` inside the `/boot/` folder of the SD that should be mounted and visible on your computer

##Installation 
1. If you already know the mac address of the controller you are going to use, put it in `config/controller-mac-address.txt`
2. Copy the pi-board folder in your `/boot/` folder on the raspberry
3. Become root via `sudo su` because accessing USB like this requires to be root and sudo commands are not enough
4. Run the script : `chmod +x /boot/pi-board/setup.sh && /boot/pi-board/setup.sh`

The raspberry will reboot.

You have a PS4 controller :
Register the service so it starts on boot :
`systemctl enable ps4-bt-controller`

You have another controller that you can connect via bluetooth:
You need to put its mac address in `config/controller-mac-address.txt`
then enable the service timer :
`systemctl enable standard-bt-controller.timer`

Reboot the device :
`reboot`

Wait a few seconds then use the pair mode on your controller : 
Hold button Xbox button for Xbox one controller
Holder share + PS button for PS4 controller

Note for PS: you will need to do this pairing after every reboot, and you should not forget to turn the controller off after use (hold PS button) to not drain the battery


