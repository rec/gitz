import os

README = 'help/README.rst'
LINK = '`{0} <{0}.rst>`_'


def main(commands):
    tmpfile = README + '.tmp'
    with open(tmpfile, 'w') as fp:
        print('gitz commands', file=fp)
        print('-------------', file=fp)

        for command, help in commands.items():
            print(file=fp)
            print(LINK.format(command), file=fp)

            summary = help[help['COMMAND']]
            for s in summary:
                print(' ', s.strip(), file=fp)

    os.rename(tmpfile, README)
