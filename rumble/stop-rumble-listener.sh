#!/bin/sh

PID=$(cat ~/.pi-board-rumbler/pid.txt)

if [ -n "$PID" ]; then
  kill -15 "$PID"
  rm ~/.pi-board-rumbler/pid.txt
fi
