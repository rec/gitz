from pathlib import Path

_HELP_DIRECTORY = Path(__file__).parent.parent.parent / 'help'


def main(commands):
    for command, help in commands.items():
        help_file = (_HELP_DIRECTORY / command).with_suffix('.rst')
        with open(help_file, 'w') as fp:
            _write(command, help, lambda *a: print(*a, file=fp))


def _write(command, help, print):
    def header(line, underline='='):
        print(line)
        print(underline * len(line))
        print()

    def print_lines(lines, *args):
        for i, line in enumerate(lines):
            if not i:
                print()
            print(*args, line)

    for field, lines in help.items():
        if field.startswith('git-'):
            header('``%s``: %s' % (field, lines[0]), '-')
            print_lines(lines, '   ')

        elif field.startswith('---'):
            print_lines(lines, '   ')

        elif field == 'USAGE':
            header(field)
            print()
            print('.. code-block:: bash')
            print_lines(lines, '   ')

        else:
            print_lines(lines, '   ')
