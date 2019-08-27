from ..program import safe_run
import setup

NONE = '(none)'
INDENT = 4
SAFE = 'safe'
DANGERS = {'safe', 'branch', 'history', 'janky'}


def read_one(command):
    help = {'COMMAND': command}
    section = NONE
    for line in safe_run(command, '-h'):
        if not line or line.startswith(' '):
            for i in range(INDENT):
                if line.startswith(' '):
                    line = line[1:]
            help.setdefault(section, []).append(line)
        elif line.endswith(':'):
            section = line[:-1]
        else:
            section = line

    for k, v in help.items():
        while v and not v[-1].strip():
            v.pop()

    return help


def read():
    command_help = {}
    for command in setup.COMMANDS:
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
