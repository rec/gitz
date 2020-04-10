from . import get_command_help
from . import screenshot
from .movies import upload
import safer

README = 'README.rst'
LINK = '`git {0} <doc/git-{0}.rst>`_'
SAFE = 'safe'
IMAGE_TAG = '.. figure::'
TARGET_TAG = '    :target:'
TAIL_TAG = 'Safe commands'


def main(commands):
    with safer.writer(README) as fp:
        all_movie_url = upload.all_movie_url()

        for line in open(README):
            ls = line.strip()
            if ls.startswith(TAIL_TAG):
                _tail(fp, _sort_by_danger(commands))
                return  # Everything after this tag is ignored.

            if ls.startswith(IMAGE_TAG):
                fp.write('%s %s.png\n' % (IMAGE_TAG, all_movie_url))
            elif ls.startswith(TARGET_TAG.strip()):
                _, query = ls.split('?')
                fp.write('%s %s?%s\n' % (TARGET_TAG, all_movie_url, query))
            else:
                fp.write(line)


def _tail(fp, command_help):
    for i, (danger, message) in enumerate(MESSAGES.items()):
        if i:
            print(file=fp)

        print(message, file=fp)
        print('=' * len(message), file=fp)
        print(file=fp)
        if danger in PRE:
            print(PRE[danger], file=fp)
            print(file=fp)

        for j, sections in enumerate(command_help.get(danger) or ()):
            if j:
                print(file=fp)
            git, command = sections['COMMAND'].split('-', maxsplit=1)
            assert git == 'git'
            print(LINK.format(command), file=fp)
            cmd = 'git ' + command
            for hc in sections[cmd]:
                print('  ' + hc, file=fp)
            screenshot.screenshot(fp, cmd)

        if danger in POST:
            print(file=fp)
            print(POST[danger], file=fp)


def _sort_by_danger(commands):
    command_help = {}
    for command, data in commands.items():
        data = get_command_help.get_one(command)
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


MESSAGES = {
    'safe': 'Safe commands',
    'branch': 'Dangerous commands that delete, rename or overwrite branches',
    'history': 'Dangerous commands that rewrite history',
}


PRE = {
    'safe': 'Informational commands that don\'t change your repository',
    'history': """\
Slice, dice, shuffle and split your commits.

These commands are not intended for use on a shared or production branch, but
can significantly speed up rapid development on private branches.""",
}

POST = {
    'branch': """\
By default, the branches ``develop`` and ``master`` are protected -
they are not allowed to be copied to, renamed, or deleted.

You can configure this in three ways:

- setting the ``--all/-a`` flag ignore protected branches entirely

- setting the environment variable ``GITZ_PROTECTED_BRANCHES`` overrides these
  defaults

- setting a value for the keys ``PROTECTED_BRANCHES`` in the file
  .gitz.json in the top directory of your Git project has the same effect"""
}
