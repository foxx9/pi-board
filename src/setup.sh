#!/bin/bash

cp isticktoit_usb.sh /usr/bin/isticktoit_usb.sh
chmod 755 /usr/bin/isticktoit_usb.sh

cp isticktoit.service /etc/systemd/system/isticktoit.service
chmod 644 /etc/systemd/system/isticktoit.service

systemctl enable isticktoit
systemctl start isticktoit
