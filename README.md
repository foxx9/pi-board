# Pi-Board project for RG350

With the support of HDMI now present on the RG350, but because controller support is non existing, I have created this project to make it possible to fake keyboard inputs with the help of a RaspberryPi Zero W, as the rg350 has all of its controls mapped to keyboard keys.


This idea is to connect the Pi to the rg350 via OTG port and make it act as a keyboard (thanks https://randomnerdtutorials.com/raspberry-pi-zero-usb-keyboard-hid/ ), then connect the controller with BT to the pi and translate controller inputs to keyboard inputs to send to the Pi.

Tested only with Ps4 dualshock and Xbox one controller 

Demo:


[![Controller input test](https://img.youtube.com/vi/TKLczUVuZvI/0.jpg)](https://www.youtube.com/watch?v=TKLczUVuZvI)

[![In game](https://img.youtube.com/vi/Mz3i_3aWrC8/0.jpg)](https://www.youtube.com/watch?v=Mz3i_3aWrC8)


## SD card setup
Here are the instructions for a fresh install of the raspbian image.
If you already have an accessible Raspberry PI ZERO W via ssh you can skip this part

1. Download and unzip this project sources
1. Flash the most recent image of Raspbian to the SD card (I used the lite version : 2020-05-27-raspios-buster-lite-armhf at this time using https://www.raspberrypi.org/downloads/) 
2. Rename  `wpa_supplicant_example.conf` to `wpa_supplicant.conf` and put your WIFI settings ( you could setup a fixed IP in your router settings, so it will be easier to SSH later )
3. Copy `ssh` and `wpa_supplicant.conf` inside the `/boot/` folder of the SD that should be mounted and visible on your computer

## Installation 
1. If you already know the mac address of the controller you are going to use, put it in `config/controller-mac-address.txt`
2. Copy the pi-board folder in your `/boot/` folder on the raspberry
3. SSH to the raspberry
4. Become root via `sudo su` because accessing USB like this requires to be root and sudo commands are not enough
5. Run the script : `chmod +x /boot/pi-board/setup.sh && /boot/pi-board/setup.sh`

The raspberry will reboot.

## Controller configuration 
 ### You have a PS4 controller :
Register the service so it starts on boot :
`systemctl enable ps4-bt-controller`

 ### You have another controller that you can connect via bluetooth:

You need to put its mac address in `config/controller-mac-address.txt`
You can retrieve the mac address by joining it to a computer and checking its settings or via bluetoohctl by starting a scan ( https://www.linux-magazine.com/Issues/2017/197/Command-Line-bluetoothctl)
then enable the service :
`systemctl enable standard-bt-controller`

Reboot the device :
`reboot`

## Connect the controller after reboot  

Wait a few seconds then use the pair mode on your controller : 
 - Hold button Xbox button for Xbox one controller, only necessary once
 - Hold share + PS button for PS4 controller, you will need to do this pairing after every reboot, and you should not forget to turn the controller off after use (hold PS button) to not drain the battery


### Rumble 

Experimental

On your rg350 : Copy `pi-board-rumble.opk` located in the rg350/rumble folder into your rg350 in `/media/data/apps`,  enable open the Pi-board rumble app located in the applications section from the device and enable rumbling


 - Does not work with PS4 controller :  https://github.com/chrippa/ds4drv#known-issueslimitations
 
Demo : 

[![Rumble app + hdmi test](https://img.youtube.com/vi/9bJ52vWhtq4/0.jpg)](https://www.youtube.com/watch?v=9bJ52vWhtq4
)



 


