#!/usr/bin/python
import os
import signal
import struct
import time
from datetime import datetime

event_haptic = os.popen(
    "cat /proc/bus/input/devices | grep haptic -A 10 | grep Handlers  | grep -o '.......$'"
).read()
event_keyboard = os.popen(
    "cat /proc/bus/input/devices | grep iSticktoit -A 10 | grep Handlers  | grep -o '.......$'"
).read()

console_fd = os.open('/dev/console', os.O_NOCTTY)

if not event_haptic:
    print("No haptic device found")
    exit()

if not event_keyboard:
    print("No Raspberry keyboard found")
    exit()

event_haptic_path = '/dev/input/' + event_haptic.rstrip().strip()
event_keyboard_path = '/dev/input/' + event_keyboard.rstrip().strip()

print("Will listen on " + event_haptic_path)

FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

EV_LED = 17

EV_FF = 21
EV_SYN = 0

LOOP = True
FCNTL_SLEEP = 0.001


def graceful_quit(signum, frame):
    global LOOP
    LOOP = False
    raise OSError("Force stop reading open files")


signal.signal(signal.SIGINT, graceful_quit)
signal.signal(signal.SIGTERM, graceful_quit)


def convert(number):
    dt = datetime.now()
    as_bin = bin(number)[2:].zfill(5)
    all = []
    for i in range(0, 5):
        all.append(struct.pack(FORMAT, dt.second, dt.microsecond, EV_LED, i, int(as_bin[len(as_bin) - 1 - i])))
    all.append(struct.pack(FORMAT, dt.second, dt.microsecond, EV_SYN, 0, 0))
    return all


def send_led_state(number):
    with open(event_keyboard_path, 'rb+') as fd:
        instructions = convert(number)
        for instruction in instructions:
            fd.write(instruction)
        time.sleep(FCNTL_SLEEP)


state_flag = True


def handle_code(c):
    global state_flag
    to_send = c | (16 if state_flag else 0)
    state_flag = not state_flag
    send_led_state(to_send)


with open(event_haptic_path, "rb") as in_file:
    event_haptic = in_file.read(EVENT_SIZE)
    while LOOP and event_haptic:
        (tv_sec, tv_usec, e_type, code, value) = struct.unpack(FORMAT, event_haptic)
        if e_type == EV_FF and value == 1:
            # we stack events of the same SYN REPORT
            handle_code(code)
        event_haptic = in_file.read(EVENT_SIZE)

os.close(console_fd)
print("Stopped")
