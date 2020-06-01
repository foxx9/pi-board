#!/usr/bin/expect -f

set address [lindex $argv 0]
set prompt "#"

spawn bluetoothctl
expect -re $prompt
send "power on\r"
expect -re $prompt
send "scan on\r"
send_user "\nSleeping\r"
sleep 30
send_user "\nDone sleeping\r"
send "scan off\r"
expect "Controller"
send "trust $address\r"
send "pair $address\r"
sleep 5

send_user "\nShould be paired now.\r"
send "exit\r"
expect eof
