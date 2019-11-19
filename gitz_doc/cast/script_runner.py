from gitz.program import run_proc
from . import constants
from . import keystrokes
from . import typing_errors
import time
import random

MAX_TIME = 1
NEW_PAGE = '\f'
EPSILON = 0.001


class ScriptRunner:
    def __init__(self, prompt):
        keystroke_times = keystrokes.all_keystrokes()
        self.keystroke_times = [k for k in keystroke_times if k < MAX_TIME]
        self.prompt = prompt

    def __call__(self, lines):
        self.results = []
        self.start_time = time.time()
        for line in lines:
            self._run_one(line)

        return self.results

    def _run_one(self, line):
        if line == NEW_PAGE:
            self._add(constants.CONTROL_L)
            return

        self.index = hash(line)
        random.seed(self.index)
        self._add(self.prompt)
        for k in typing_errors.with_errors(line):
            self._add_key(constants.RETURN if k == '\n' else k)

        try:
            run_proc.run_proc(line.strip(), self._add, self._add, shell=True)
        except Exception:
            pass

    def _add(self, item):
        dt = time.time() - self.start_time
        if dt < EPSILON:
            dt = 0
        self.results.append([dt, 'o', item])

    def _add_key(self, key):
        self.index %= len(self.keystroke_times)
        self.start_time -= self.keystroke_times[self.index]
        self.index += 1
        self._add(key)


if __name__ == '__main__':
    import json
    import sys

    header = {'version': 2, 'width': 80, 'height': 32}
    print(json.dumps(header), file=sys.stdout)

    runner = ScriptRunner('/foo/bar$ ')
    with open('gitz_doc/cast/scripts/test.sh') as fp:
        for line in runner(fp):
            print(json.dumps(line), file=sys.stdout)
