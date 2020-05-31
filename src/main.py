#!/usr/bin/env python3

import copy
# !/usr/bin/python
import struct
import sys
from functools import cmp_to_key

KeyboardMapping = {
    'right': 0x4f,
    'left': 0x50,
    'down': 0x51,
    'up': 0x52,
    'dividePav': 0x54,
    'deleteNumPav': 0x63,
    'enter': 0x28,
    'escape': 0x29,
    'pageDown': 0x4e,
    'pageUp': 0x4b,
    'backspace': 0x2a,
    'tab': 0x2b,
    'home': 0x4a,
    'space': 0x2c
}
Modifiers = {
    'leftControl': 0,
    'leftShift': 1,
    'leftAlt': 2,
    'leftGUI': 3,
    'rightControl': 4,
    'rightShift': 5,
    'rightAlt': 6,
    'rightGUI': 7,
}

ControllerMapping = {
    'a': 'leftAlt',
    'b': 'leftControl',
    'x': 'leftShift',
    'y': 'space',
    'start': 'enter',
    'select': 'escape',
    'l1': 'tab',
    'r1': 'backspace',
    'l2': 'pageUp',
    'r2': 'pageDown',
    'l3': 'dividePav',
    'r3': 'deleteNumPav',
    'home': 'home',
    'right': 'right',
    'left': 'left',
    'down': 'down',
    'up': 'up'
}

KeyCodeMapping = {
    172: 'home',
    304: 'a',
    305: 'b',
    307: 'x',
    308: 'y',
    310: 'l1',
    311: 'r1',
    158: 'select',
    315: 'start',
    317: 'l3',
    318: 'r3',
}


class State:
    def __init__(self):
        self.a = False
        self.b = False
        self.x = False
        self.y = False
        self.start = False
        self.select = False
        self.home = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.l1 = False
        self.l2 = False
        self.l3 = False
        self.r1 = False
        self.r2 = False
        self.r3 = False

    def __eq__(self, other):
        if isinstance(other, State):
            return self.a == other.a and \
                   self.b == other.b and \
                   self.x == other.x and \
                   self.y == other.y and \
                   self.start == other.start and \
                   self.select == other.select and \
                   self.home == other.home and \
                   self.left == other.left and \
                   self.right == other.right and \
                   self.up == other.up and \
                   self.down == other.down and \
                   self.l1 == other.l1 and \
                   self.l2 == other.l2 and \
                   self.l3 == other.l3 and \
                   self.r1 == other.r1 and \
                   self.r2 == other.r2 and \
                   self.r3 == other.r3
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


def sort_predicate(last_report):
    def compare(a, b):
        a_was_there = a in last_report
        b_was_there = b in last_report

        if a_was_there and b_was_there:
            return last_report.index(a) - last_report.index(b)
        elif not a_was_there and not b_was_there:
            return 0
        elif a_was_there:
            return -1
        else:
            return 1

    return compare


def build_report(state, last_report):
    modifier = 0
    pressed = []
    for key in vars(state):
        if getattr(state, key, False):
            mapping = ControllerMapping[key]
            if mapping in Modifiers:
                power = Modifiers[mapping]
                modifier += pow(2, power)
            elif mapping in KeyboardMapping:
                pressed.append(KeyboardMapping[mapping])

    # we can only keep 6 pressed at the same time
    pressed = pressed[:6]

    if last_report is not None:
        sub = last_report[2:6]
        pressed = sorted(pressed, key=cmp_to_key(sort_predicate(sub)))

    while len(pressed) < 6:
        pressed.append(0)

    report = [modifier, 0] + pressed
    print(report)
    return report


def trigger_active(value):
    return value > 1024 / 30


def positive_value_axis(value):
    return value > 32768 + 32768 * 0.5


def negative_value_axis(value):
    return value < 32768 - 32768 * 0.5


def send_report_to_keyboard(path, report):
    with open(path, 'rb+') as fd:
        fd.write(bytes(report))


def startLoop():
    usb_path = "/dev/hidg0"
    # usb_path = "./text.txt"
    infile_path = "/dev/input/event" + (sys.argv[1] if len(sys.argv) > 1 else "0")

    """
    FORMAT represents the format used by linux kernel input event struct
    See https://github.com/torvalds/linux/blob/v5.5-rc5/include/uapi/linux/input.h#L28
    Stands for: long int, long int, unsigned short, unsigned short, unsigned int
    """
    FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(FORMAT)

    # open file in binary mode
    with open(infile_path, "rb") as in_file:

        event = in_file.read(EVENT_SIZE)
        last_state = State()
        last_report = None
        while event:
            (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

            if type == 1 or type == 3:
                #    print("Event type %u, code %u, value %u at %d.%d" % \
                #          (type, code, value, tv_sec, tv_usec))
                new_state = copy.copy(last_state)

                # button pressed
                if type == 1:
                    if code in KeyCodeMapping:
                        setattr(new_state, KeyCodeMapping[code], value == 1)
                elif type == 3:
                    if code == 16:
                        new_state.left = value != 1 and value != 0
                        new_state.right = value == 1
                    elif code == 17:
                        new_state.up = value != 1 and value != 0
                        new_state.down = value == 1
                    elif code == 0:
                        new_state.left = negative_value_axis(value)
                        new_state.right = positive_value_axis(value)
                    elif code == 1:
                        new_state.up = negative_value_axis(value)
                        new_state.down = positive_value_axis(value)
                    elif code == 10:
                        new_state.l2 = trigger_active(value)
                    elif code == 9:
                        new_state.r2 = trigger_active(value)
                    # code 3 and 4 are right stick

                if new_state != last_state:
                    #      print("changed")
                    print(vars(new_state))
                    report = build_report(new_state, last_report)
                    print(bytes(report))

                    send_report_to_keyboard(usb_path, report)
                    last_report = report
                    last_state = new_state

            # else:
            #     # Events with code, type and value == 0 are "separator" events
            #     print("===========================================")

            event = in_file.read(EVENT_SIZE)


def checkMapping():
    for button, mappedKey in ControllerMapping.items():
        if (mappedKey not in KeyboardMapping) and (mappedKey not in Modifiers):
            print(mappedKey, 'has no mapping')


checkMapping()
startLoop()
