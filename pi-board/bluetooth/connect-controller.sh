#!/bin/bash

value=$(</boot/pi-board/config/controller-mac-address.txt)
cd /boot/pi-board/bluetooth/ || exit

while true; do
  if [ -z "$value" ]; then
    echo "Your did not set a controller mac address"
    exit
  else
    echo "Using mac address : $value"
    if echo $(hcitool con) | grep -q "$value"; then
      echo "Controller is connected"
    else
      if echo $(/usr/bin/expect ./expect-see-paired.sh) | grep -q "$value"; then
        echo "Attempt to connect"
        /usr/bin/expect ./expect-connect.sh "$value"
      else
        echo "Attempt to pair"
        /usr/bin/expect ./expect-pair.sh "$value"
      fi

    fi
  fi
  sleep 5
done
