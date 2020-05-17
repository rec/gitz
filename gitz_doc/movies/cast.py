"""
Represents a single asciinema file
"""

from . import constants
from pathlib import Path
import json
import safer

EXIT = 'exit' + constants.RETURN
EPSILON = 0.001


class Cast:
    def __init__(self, lines=None, header=None):
        self.lines = lines or []
        self.header = constants.HEADER if header is None else header

    @classmethod
    def read(cls, fp):
        if isinstance(fp, (str, Path)):
            with open(fp) as fp2:
                return cls.read(fp2)

        lines = []

        for i, line in enumerate(fp):
            value = json.loads(line)
            if i:
                assert isinstance(value, list)
                lines.append(value)
            else:
                assert isinstance(value, dict)
                header = value
        return cls(lines, header)

    def append(self, keys, delta_time):
        dt = 0 if delta_time < EPSILON else delta_time
        self.lines.append([dt, 'o', keys])

    def write(self, fp):
        if isinstance(fp, (str, Path)):
            with safer.writer(fp) as fp2:
                return self.write(fp2)

        for i in (self.header, *self.lines):
            print(json.dumps(i), file=fp)

    def scale(self, ratio):
        for line in self.lines:
            line[0] *= ratio

    def replace_prompt(self):
        original = self.lines[0][2]
        for line in self.lines:
            line[2] = line[2].replace(original, constants.PROMPT, 1)

    def remove_exit(self):
        last = self.lines[-1]
        if last[2] == EXIT:
            last[2] = last[2][4:]

    def update(self, other, offset=0):
        for c in 'width', 'height':
            s = self.header.get(c, 0)
            o = other.header.get(c, 0)
            m = max(s, o)
            if m > 0:
                self.header[c] = m

        if self.lines:
            offset += self.lines[-1][0]
        self.lines.extend([t + offset, i, k] for t, i, k in other.lines)
