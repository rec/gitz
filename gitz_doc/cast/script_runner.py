from gitz.program import run_proc
from . import constants
from . import keystrokes
from . import typing_errors
import json
import sys
import time

MAX_TIME = 1
NEW_PAGE = '\f'
EPSILON = 0.001
TIME_TO_THINK = 2
TIME_TO_READ_ONE_CHAR = 0.005
TIME_SCALE = 0.70
HEADER = {'version': 2, 'width': 80, 'height': 32}


class ScriptRunner:
    def __init__(self):
        keystroke_times = keystrokes.all_keystrokes()
        keystroke_times = [TIME_SCALE * k for k in keystroke_times]
        self.keystroke_times = [k for k in keystroke_times if k < MAX_TIME]

    def __call__(self, script):
        self.results = [constants.HEADER]
        self.start_time = time.time()
        self._add(constants.PROMPT)
        for line in script:
            self._run_one(line)

        return self.results

    def _run_one(self, line):
        if line == NEW_PAGE:
            self._add(constants.CONTROL_L)
            return

        self.index = hash(line)
        for k in typing_errors.with_errors(line):
            self._add_key(constants.RETURN if k == '\n' else k)

        before = len(self.results)
        self._run(line.strip())
        chars = sum(len(x[2]) for x in self.results[before + 1:])

        self._add(constants.PROMPT)

        self.start_time -= TIME_TO_THINK + chars * TIME_TO_READ_ONE_CHAR
        self._add('')

    def _run(self, cmd):
        try:
            run_proc.run_proc(cmd, self._add_line, self._add_line, shell=True)
        except Exception:
            pass  # Already reported in _add_line

    def _add(self, item):
        dt = time.time() - self.start_time
        if dt < EPSILON:
            dt = 0
        self.results.append([dt, 'o', item])

    def _add_line(self, line):
        self._add(line)
        self._add(constants.RETURN)

    def _add_key(self, key):
        self.index %= len(self.keystroke_times)
        self.start_time -= self.keystroke_times[self.index]
        self.index += 1
        self._add(key)


def run_script(script, file=sys.stdout):
    runner = ScriptRunner(constants.PROMPT)
    with open(script) as fp:
        for line in runner(fp):
            print(json.dumps(line), file=file)


if __name__ == '__main__':
    run_script('gitz_doc/cast/scripts/test.sh')
