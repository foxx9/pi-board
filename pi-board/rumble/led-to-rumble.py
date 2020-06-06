import signal

from evdev import ecodes, InputDevice, ff

dev = InputDevice('/dev/input/event0')


def graceful_quit(signum, frame):
    global LOOP
    LOOP = False


signal.signal(signal.SIGINT, graceful_quit)
signal.signal(signal.SIGTERM, graceful_quit)


def create_effect(strong, weak):
    return ff.Effect(
        ecodes.FF_RUMBLE, -1, 0,
        ff.Trigger(0, 0),
        ff.Replay(17, 0),
        ff.EffectType(ff_rumble_effect=ff.Rumble(strong_magnitude=strong, weak_magnitude=weak))
    )


multiplier_weak = int(0xffff / 8)
multiplier_strong = int(multiplier_weak / 4)
repeat = 8

effects = [None] * 8
for i in range(8):
    effects[i] = dev.upload_effect(create_effect(i * multiplier_strong, i * multiplier_weak))

WeirdMap = {
    6: 3,
    5: 6,
    4: 2,
    3: 5,
    2: 1,
    1: 4
}

LOOP = True
with open('/dev/hidg0', "rb") as in_file:
    event = in_file.read(1)
    while LOOP and event:
        value = int.from_bytes(event, byteorder='big')
        if value in WeirdMap:
            value = WeirdMap[value]
        dev.write(ecodes.EV_FF, effects[value], repeat)

        print(value)
        event = in_file.read(1)

for i in range(len(effects)):
    dev.erase_effect(i)
