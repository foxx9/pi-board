#!/usr/bin/python
import fcntl
import os
import signal
import struct

event_path = '/dev/input/event1'
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

EV_FF = 21

FORCE_EMPTY = 0
FORCE_LOW = 1
FORCE_MIDDLE = 2
FORCE_HIGH = 4

KDSETLED = 0x4B32
LOOP = True


def graceful_quit():
    global LOOP
    LOOP = False


signal.signal(signal.SIGINT, graceful_quit)
signal.signal(signal.SIGTERM, graceful_quit)


def send_led_state(led):
    fcntl.ioctl(console_fd, KDSETLED, led)


def map_code(c):
    if c == 0:
        return 0
    elif c < 7:
        return FORCE_LOW
    elif c < 15:
        return FORCE_MIDDLE
    else:
        return FORCE_HIGH


def handle_code(c):
    force = map_code(c)
    if force is not FORCE_EMPTY:
        send_led_state(force)


with os.open('/dev/console', os.O_NOCTTY) as console_fd:
    with open(event_path, "rb") as in_file:
        event = in_file.read(EVENT_SIZE)
        while LOOP and event:
            (tv_sec, tv_usec, e_type, code, value) = struct.unpack(FORMAT, event)
            if e_type == EV_FF and value == 1:
                handle_code(code)
