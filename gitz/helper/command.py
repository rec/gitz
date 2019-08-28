from pathlib import Path

_HELP_DIRECTORY = Path(__file__).parent.parent.parent / 'help'


def main(commands):
    for command, help in commands.items():
        help_file = (_HELP_DIRECTORY / command).with_suffix('.rst')
        with open(help_file, 'w') as fp:
            _write(command, help, lambda *a: print(*a, file=fp))
        return


def _write(command, help, _print):
    def header(line, underline='='):
        _print(line)
        _print(underline * len(line))

    def print_lines(lines, *args):
        for i, line in enumerate(lines):
            if not i:
                _print()
            _print(*args, line)

    for field, lines in help.items():
        if field.startswith('git-'):
            header('``%s``: %s' % (field, lines[0]), '-')
            print_lines(lines[1:], '   ')

        elif field.startswith('---'):
            _print()
            header('FLAGS')
            print_lines(lines, '   ')

        elif field == 'COMMAND':
            continue

        elif field == 'USAGE':
            _print()
            header(field)
            _print('.. code-block:: bash')
            print_lines(lines, '   ')

        else:
            _print()
            header(field)
            print_lines(lines, '   ')
