from pathlib import Path

_HELP_DIRECTORY = Path(__file__).parent.parent.parent / 'help'


def main(commands):
    for command, help in commands.items():
        help_file = (_HELP_DIRECTORY / command).with_suffix('.rst')
        with open(help_file, 'w') as fp:
            Writer(command, help, fp).write()


class Writer:
    def __init__(self, command, help, fp):
        self.command = command
        self.help = help
        self.fp = fp

    def write(self):
        for field, lines in self.help.items():
            if field.startswith('git-'):
                field = 'TITLE'
            elif field.startswith('---'):
                field = 'FLAGS'
            method = getattr(self, '_' + field.lower(), None)
            if method:
                method(lines)
            else:
                self._default(field, lines)

    def _title(self, lines):
        self._header('``%s``: %s' % (self.command, lines[0]), '-')
        self._print_lines(lines[1:])

    def _command(self, lines):
        pass

    def _usage(self, lines):
        self._print()
        self._header('USAGE')
        self._print('.. code-block:: bash')
        self._print_lines(lines)

    def _default(self, field, lines):
        self._print()
        self._header(field)
        self._print_lines(lines)

    def _print(self, *args):
        print(*args, file=self.fp)

    def _header(self, line, underline='='):
        self._print(line)
        self._print(underline * len(line))

    def _print_lines(self, lines):
        if lines:
            self._print()
        for line in lines:
            self._print('   ', line)
