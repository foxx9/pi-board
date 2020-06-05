#!/bin/sh

PID=$(cat ~/.pi-board-rumbler/pid.txt)

if [ -n "$PID" ]; then
  kill -9 "$PID"
  rm ~/.pi-board-rumbler/pid.txt
fi
