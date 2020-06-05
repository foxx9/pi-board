#!/usr/bin/python
import fcntl
import os
import signal
import struct

event = os.popen('cat /proc/bus/input/devices | grep haptic -A 10 | grep Handlers |  cut -f2 -d"="').read()

if not event:
    print("No haptic device found")
    exit()

event_path = '/dev/input/' + event.rstrip().strip()

print("Will listen on " + event_path)

FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

EV_FF = 21
EV_SYN = 0

FORCE_EMPTY = 0x00
FORCE_LOW = 0x01
FORCE_MIDDLE = 0x02
FORCE_HIGH = 0x04

KDSETLED = 0x4B32
LOOP = True


def graceful_quit(signum, frame):
    global LOOP
    LOOP = False
    raise OSError("Force stop reading open files")


signal.signal(signal.SIGINT, graceful_quit)
signal.signal(signal.SIGTERM, graceful_quit)


def send_led_state(led):
    fcntl.ioctl(console_fd, KDSETLED, led)


def map_code(c):
    if c == 0:
        return FORCE_EMPTY
    elif c < 7:
        return FORCE_LOW
    elif c < 15:
        return FORCE_MIDDLE
    else:
        return FORCE_HIGH


def handle_code(c):
    if c != 0:
        send_led_state(c)


console_fd = os.open('/dev/console', os.O_NOCTTY)
current_code = 0
with open(event_path, "rb") as in_file:
    event = in_file.read(EVENT_SIZE)
    while LOOP and event:
        (tv_sec, tv_usec, e_type, code, value) = struct.unpack(FORMAT, event)
        if e_type == EV_FF and value == 1:
            # we stack events of the same SYN REPORT
            current_code = current_code | map_code(code)
        elif e_type == EV_SYN:
            # print('should send' + str(current_code))
            handle_code(current_code)
            current_code = 0
        event = in_file.read(EVENT_SIZE)

os.close(console_fd)
print("Stopped")
