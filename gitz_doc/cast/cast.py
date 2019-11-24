from . import constants
import json

EXIT = 'exit' + constants.RETURN


class Cast:
    def __init__(self, lines=None, header=None):
        self.lines = lines or []
        self.header = header or {'version': 2}

    @classmethod
    def read(cls, filename):
        lines = []

        with open(filename) as fp:
            for i, line in enumerate(fp):
                value = json.loads(line)
                if i:
                    assert isinstance(value, list)
                    lines.append(value)
                else:
                    assert isinstance(value, dict)
                    header = value
        return cls(lines, header)

    def write(self, filename):
        with open(filename, 'w') as fp:
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

    def merge(self, other, offset=0):
        for c in 'width', 'height':
            s = self.header.get(c, 0)
            o = other.header.get(c, 0)
            m = max(s, o)
            if m > 0:
                self.header[c] = m

        if self.lines:
            offset += self.lines[-1][0]
        self.lines.extend([t + offset, i, k] for t, i, k in other.lines)
