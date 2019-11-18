from gitz.program import run_proc
from . import constants
from . import keystrokes
import time
import random

MAX_TIME = 1
NEW_PAGE = '\f'
ERROR_RATE = 0.10
EPSILON = 0.001


def run(lines, prompt):
    keystroke_times = [k for k in keystrokes.all_keystrokes() if k < MAX_TIME]
    results = []
    start_time = time.time()

    def append(item):
        dt = time.time() - start_time
        if dt < EPSILON:
            dt = 0
        results.append([dt, 'o', item])

    for line in lines:
        if line == NEW_PAGE:
            append(constants.CONTROL_L)
            continue

        index = hash(line)

        def append_key(key):
            nonlocal index, start_time
            index %= len(keystroke_times)
            start_time -= keystroke_times[index]
            index += 1
            append(key)

        random.seed(index)

        append(prompt)
        for k in line:
            if k == '\n':
                k = constants.RETURN
            if random.random() < ERROR_RATE:
                errors = ERRORS.get(k)
                if errors:
                    append_key(random.choice(errors))
                    append_key(constants.BACKSPACE)
            append_key(k)

        try:
            run_proc.run_proc(line.strip(), append, append, shell=True)
        except Exception:
            pass

    return results


ERRORS = {
    'a': 'qzs',
    'b': ' vfghn',
    'c': ' xsdfv',
    'd': 'werfvcxs',
    'e': 'rfdsw',
    'f': 'ertgbvcd',
    'g': 'frtyhnbv',
    'h': 'gtyujmnb',
    'i': 'u789olkj',
    'j': 'hyuikmnh',
    'k': 'juiol,mj',
    'l': 'kiop;.,',
    'm': 'nhjk, ',
    'n': 'bghjm ',
    'o': 'oikl;p',
    'p': 'ol;\'[-',
    'q': 'wa',
    'r': 'edfgt',
    's': 'aqwedcxz',
    't': 'rfghy',
    'u': 'yhjki',
    'v': 'cdfgb ',
    'w': 'qasde',
    'x': 'zasdc ',
    'y': 'tghju',
    'z': 'asx',
    '0': '9-',
    '1': '`2',
    '2': '13',
    '3': '24',
    '4': '35',
    '5': '46',
    '6': '57',
    '7': '68',
    '8': '79',
    '9': '80',
}


if __name__ == '__main__':
    for line in run(open('gitz_doc/cast/scripts/test.sh'), '/foo/bar$ '):
        print(line)
