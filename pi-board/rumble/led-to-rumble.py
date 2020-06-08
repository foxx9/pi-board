import math
import signal

from evdev import ecodes, InputDevice, ff

dev = InputDevice('/dev/input/event0')


def graceful_quit(signum, frame):
    global LOOP
    LOOP = False
    raise OSError("Force stop reading open files")


signal.signal(signal.SIGINT, graceful_quit)
signal.signal(signal.SIGTERM, graceful_quit)


def create_effect(strong, weak):
    return ff.Effect(
        ecodes.FF_RUMBLE, -1, 0,
        ff.Trigger(0, 0),
        ff.Replay(17, 0),
        ff.EffectType(ff_rumble_effect=ff.Rumble(strong_magnitude=strong, weak_magnitude=weak))
    )


def ease_function(x):
    return -(math.cos(math.pi * x) - 1) / 2


SHAKE_RUMBLE_STRONG_MAGNITUDE_MAX = 0x7FFF
SHAKE_RUMBLE_WEAK_MAGNITUDE_MAX = 0x7FFFF

effects = []
for i in range(16):
    print("registering event " + str(i))
    # from  https://github.com/soarqin/RG350_pcsx4all/blob/master/src/port/sdl/port.cpp
    weak = int(SHAKE_RUMBLE_WEAK_MAGNITUDE_MAX * ease_function((i + 1) / 16))
    # Only enable the strong motor with greater than 7 events
    if i > 7:
        strong = int(SHAKE_RUMBLE_STRONG_MAGNITUDE_MAX * ease_function((i + 1 - 8) / 8))
    else:
        strong = 0
    effects.append(dev.upload_effect(create_effect(strong, weak)))

LOOP = True
with open('/dev/hidg0', "rb") as in_file:
    event = in_file.read(1)
    while LOOP and event:
        value = int.from_bytes(event, byteorder='big')
        value = value & 15  # bitwise to only keep the right value
        dev.write(ecodes.EV_FF, effects[value], 1)
        event = in_file.read(1)

# for i in range(len(effects)):
#    dev.erase_effect(i)
