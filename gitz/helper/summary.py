from pathlib import Path
from ..program import PROGRAM
from . import reader
import os

README = 'README.rst'


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
    tmpfile = README + '.tmp'
    with open(tmpfile, 'w') as fp:
        for line in open(README):
            if line.startswith('Safe commands'):
                summary(fp, reader.read())
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
assert set(MESSAGES) == set(reader.DANGERS)


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
    PROGRAM.initialize()
    main()
