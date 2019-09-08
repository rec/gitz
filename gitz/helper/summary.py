from . import reader
from . import screenshot
import os

README = 'README.rst'
LINK = '`{0} <doc/{0}.rst>`_'
SAFE = 'safe'


def summary(fp, command_help):
    for i, (danger, message) in enumerate(MESSAGES.items()):
        if i:
            print(file=fp)

        print(message, file=fp)
        print('=' * len(message), file=fp)
        print(file=fp)
        if danger in PRE:
            print(PRE[danger], file=fp)
            print(file=fp)

        for j, sections in enumerate(command_help[danger]):
            if j:
                print(file=fp)
            command = sections['COMMAND'].replace('git-', 'git ')
            print(LINK.format(command), file=fp)
            for hc in sections[command]:
                print('  ' + hc, file=fp)
            screenshot.screenshot(fp, command)

        if danger in POST:
            print(file=fp)
            print(POST[danger], file=fp)


def sort_by_danger(commands):
    command_help = {}
    for command, data in commands.items():
        data = reader.read_one(command)
        danger = data.get('DANGER', '')
        if danger:
            for d in MESSAGES:
                if d in danger[0]:
                    command_help.setdefault(d, []).append(data)
                    break
            else:
                raise ValueError('Bad danger', danger[0])
        else:
            command_help.setdefault(SAFE, []).append(data)
    return command_help


def main(commands):
    tmpfile = README + '.tmp'
    with open(tmpfile, 'w') as fp:
        for line in open(README):
            if not line.startswith('Safe commands'):
                fp.write(line)
            else:
                summary(fp, sort_by_danger(commands))
                break
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
Slice, dice, shuffle and split your commits.

These commands are not intended for use on a shared or production branch, but
can significantly speed up rapid development on private branches.""",
    'janky': """\
``git-all`` is something I use all the time, but it only works in
simple cases, and I don't see a good path to making it do complicated
things in a sane way.""",
}

POST = {
    'branch': """\
By default, the branches ``develop`` and ``master`` and the remote ``upstream``
are protected - they are not allowed to be copied to, renamed, or deleted.

You can configure this in three ways:

- setting the ``--all/-a`` flag ignore protected branches entirely

- setting one of the the environment variables
  ``GITZ_PROTECTED_BRANCHES`` or ``GITZ_PROTECTED_REMOTES`` overrides these
  defaults

- setting a value for the keys ``PROTECTED_BRANCHES`` or ``PROTECTED_REMOTES``
  in the file .gitz.json in the top directory of your Git project"""
}
