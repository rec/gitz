from .. import config
from ..program import safe_run

NONE = '(none)'
INDENT = 4
SAFE = 'safe'
DANGERS = {'safe', 'branch', 'history', 'janky'}
FULL_USAGE = '---'


def read_one(command):
    full_usage = False
    help = {'COMMAND': command}
    section = NONE
    for line in safe_run(command, '-h'):
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


def sort_by_danger(commands):
    command_help = {}
    for command, data in commands.items():
        data = read_one(command)
        danger = data.get('DANGER', '')
        if danger:
            for d in DANGERS:
                if d in danger[0]:
                    command_help.setdefault(d, []).append(data)
                    break
            else:
                raise ValueError('Bad danger', danger[0])
        else:
            command_help.setdefault(SAFE, []).append(data)
    return command_help
