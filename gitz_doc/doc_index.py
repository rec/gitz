import safer

README = 'doc/README.rst'
LINK = '`{0} <{0}.rst>`_'
HOME_LINK = '`Gitz home page <https://github.com/rec/gitz/>`_'


def main(commands):
    with safer.writer(README) as fp:
        print('gitz commands', file=fp)
        print('-------------', file=fp)

        for command, help in commands.items():
            print(file=fp)
            print(LINK.format(command), file=fp)

            summary = help[help['COMMAND'].replace('git-', 'git ')]
            for s in summary:
                print(' ', s.strip(), file=fp)
        print(file=fp)
        print(HOME_LINK, file=fp)
        print('=' * len(HOME_LINK), file=fp)
