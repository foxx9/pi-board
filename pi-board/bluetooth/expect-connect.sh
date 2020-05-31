#!/usr/bin/expect -f

set address [lindex $argv 0]

set prompt "#"

spawn bluetoothctl
expect -re $prompt
send "connect $address\r"
sleep 5
send_user "\nShould be connected now.\r"
expect -re $prompt
send "exit\r"
expect eof
