#!/usr/bin/expect -f

spawn bluetoothctl
expect -re "#"
send "paired-devices\r"
send "exit\r"
expect eof
