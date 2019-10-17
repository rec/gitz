from .. import config
from ..runner import RUN

NONE = '(none)'
INDENT = 4
FULL_USAGE = '---'


def read_one(command):
    full_usage = False
    help = {'COMMAND': command}
    section = NONE
    for line in RUN(command, '-h', info=True):
        if full_usage:
            help.setdefault(section, []).append(line)

        elif not line or line.startswith(' '):
            for i in range(INDENT):
                if line.startswith(' '):
                    line = line[1:]
            help.setdefault(section, []).append(line)

        elif line.startswith(FULL_USAGE):
            full_usage = True
            section = FULL_USAGE

        elif line.endswith(':'):
            section = line[:-1]

        else:
            section = line

    for k, v in help.items():
        while v and not v[-1].strip():
            v.pop()
        while v and not v[0].strip():
            v.pop(0)

    return help


def read():
    return {c: read_one(c) for c in config.COMMANDS}
