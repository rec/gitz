from . import constants
from . import cast
import statistics

ACCEPTED_KEYS = {constants.BACKSPACE, constants.RETURN}
TIMES = (
    [0.217, 0.103, 0.112, 0.177, 0.072, 0.16, 0.072, 0.184]
    + [0.104, 0.159, 0.225, 0.328, 0.321, 0.591, 0.168, 0.08]
    + [0.099, 0.11, 0.064, 0.209, 0.127, 0.288, 0.047, 0.16]
    + [0.384, 0.175, 0.05, 0.136, 0.296, 0.225, 0.295]
)


def keystroke_times(lines):
    last_time = None
    for t_k in lines:
        time, _, keys = t_k
        if len(keys) == 1 or keys in ACCEPTED_KEYS:
            if last_time is not None:
                yield time - last_time
            last_time = time
        else:
            last_time = None


def all_keystrokes():
    data = []
    for f in constants.cast_files():
        lines = cast.Cast.read(f).lines
        data.extend(keystroke_times(lines))

    print(statistics.mean(data), statistics.stdev(data))
    print()
    for d in data:
        print(round(d, 3))


def fake_text(text, prompt, delay=0):
    index = hash(text) % len(TIMES)
    entries = [prompt, ''] + list(text) + [constants.RETURN]

    time = 0
    lines = []
    for i, e in enumerate(entries):
        lines.append([time, 'o', e])
        time += TIMES[(index + i) % len(TIMES)]

    if delay:
        lines.append([time + delay, 'o', ''])
    return cast.Cast(lines)


if __name__ == '__main__':
    all_keystrokes()
