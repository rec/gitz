from gitz.program import run_proc

NONE = '(none)'
INDENT = 4
FULL_USAGE = '---'


def get_one(command):
    full_usage = False
    help = {'COMMAND': command}
    section = NONE
    lines = run_proc.run_proc((command, '-h'))
    for line in lines:
        if full_usage:
            help.setdefault(section, []).append(line)

        elif not line or line.startswith(' '):
            for _ in range(INDENT):
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


def get_command_help(commands):
    return {c: get_one(c) for c in commands}
