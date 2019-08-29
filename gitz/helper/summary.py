from . import screenshot
from . import reader
import os

README = 'README.rst'
LINK = '`{0} <doc/{0}.rst>`_'


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
            print(LINK.format(command), file=fp)
            for hc in help[command]:
                print('  ' + hc, file=fp)
            screenshot.screenshot(fp, command)

        if danger in POST:
            print(file=fp)
            print(POST[danger], file=fp)


def main(commands):
    tmpfile = README + '.tmp'
    with open(tmpfile, 'w') as fp:
        for line in open(README):
            if not line.startswith('Safe commands'):
                fp.write(line)
            else:
                summary(fp, reader.sort_by_danger(commands))
                break
    os.rename(tmpfile, README)


MESSAGES = {
    'safe': 'Safe commands',
    'branch': 'Dangerous commands that delete, rename or overwrite branches',
    'history': 'Dangerous commands that rewrite history',
    'janky': 'Dangerous commands that are janky',
}
assert set(MESSAGES) == reader.DANGERS


PRE = {
    'safe': 'Informational commands that don\'t change your repository',
    'history': """\
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
are not allowed to be copied, renamed, or deleted.

You can disable this by setting the ``--all/-a`` flag, or you can override the
protected branches or remotes by setting the environment variables
``PROTECTED_BRANCHES`` or ``PROTECTED_REMOTES``"""
}
