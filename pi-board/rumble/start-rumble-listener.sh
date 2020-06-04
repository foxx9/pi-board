#!/bin/sh

mkdir -p ~/.pi-board-rumbler

/bin/sh ./stop-rumble-listener.sh

# starts the python script that will react to rumble
nohup python rumble-listener.py >/dev/null 2>&1 &
PID=$!
mkdir -p ~/.pi-board-rumbler
echo $PID >~/.pi-board-rumbler/pid.txt
