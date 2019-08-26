from pathlib import Path
from .program import PROGRAM
from .program import safe_run
import os
import setup

NONE = '(none)'
INDENT = 4
SAFE = 'safe'
README = 'README.rst'


def parse_one(command):
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


def parse_all():
    command_help = {}
    for command in setup.COMMANDS:
        data = parse_one(command)
        danger = data.get('DANGER', '')
        if danger:
            for m in MESSAGES:
                if m in danger[0]:
                    command_help.setdefault(m, []).append(data)
                    break
            else:
                raise ValueError('Bad danger', danger[0])
        else:
            command_help.setdefault(SAFE, []).append(data)
    return command_help


def write_summary(fp, command_help):
    for i, (danger, message) in enumerate(MESSAGES.items()):
        if i:
            print(file=fp)

        print(message, file=fp)
        print('=' * len(message), file=fp)
        print(file=fp)
        if danger in PRE:
            print(PRE[danger], file=fp)
            print(file=fp)

        for j, help in enumerate(command_help[danger]):
            if j:
                print(file=fp)
            command = help['COMMAND']
            print('``%s``' % command, file=fp)
            for hc in help[command]:
                print('  ' + hc, file=fp)
            screenshot = 'img/%s-screenshot.png' % command
            if Path(screenshot).exists():
                print(file=fp)
                print('.. image::', screenshot, file=fp)

        if danger in POST:
            print(file=fp)
            print(POST[danger], file=fp)


def main():
    PROGRAM.initialize()
    tmpfile = README + '.tmp'
    with open(tmpfile, 'w') as fp:
        for line in open(README):
            if line.startswith('Safe commands'):
                write_summary(fp, parse_all())
                break
            else:
                fp.write(line)
    os.rename(tmpfile, README)


MESSAGES = {
    'safe': 'Safe commands',
    'branch': 'Dangerous commands that delete, rename or overwrite branches',
    'history': 'Dangerous commands that rewrite history',
    'janky': 'Dangerous commands that are janky',
}

PRE = {
    'safe': 'Informational commands that don\'t change your repository',
    'history': """\
These commands are not intended for use on a shared or production branch, but
can significantly speed up rapid development on private branches.""",
    'janky': """\
``git-all`` is something I use all the time, but it only works in
simple cases, and I don't see a good path to making it do complicated
things in a sane way."""
}

POST = {
    'branch': """\
By default, the branches ``develop`` and ``master`` and the remote ``upstream``
are not allowed to be copied, renamed, or deleted.

You can disable this by setting the ``--all/-a`` flag, or you can override the
protected branches or remotes by setting the environment variables
``PROTECTED_BRANCHES`` or ``PROTECTED_REMOTES``"""
}


if __name__ == '__main__':
    main()
