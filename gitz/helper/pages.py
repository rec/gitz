from pathlib import Path

_HELP_DIRECTORY = Path(__file__).parent.parent.parent / 'doc'
_COMMANDS = ()
_HOME_LINK = '`Gitz home page <https://github.com/rec/gitz/>`_'


def main(commands):
    for command, help in commands.items():
        if _COMMANDS and command not in _COMMANDS:
            continue
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

        self._print()
        self._header(_HOME_LINK)

    def _title(self, lines):
        self._header('``%s``: %s' % (self.command, lines[0]), '-')
        self._print_lines(lines[1:])

    def _examples(self, lines):
        self._print()
        self._header('EXAMPLES')
        if lines:
            self._print()
        for line in lines:
            if not line:
                self._print()
            elif line.startswith(' '):
                self._print(line)
            else:
                self._print('``%s``' % line)

    def _flags(self, lines):
        self._print()
        self._header('FLAGS')
        state = None
        optionals = []
        usage = []

        def set_state(new_state):
            nonlocal state
            state = new_state
            if usage:
                self._code_block(usage)
                self._print()
                usage.clear()
            self._print(new_state.capitalize())

        for line in lines:
            if not line:
                self._print()

            elif line.startswith(_FULL_USAGE):
                assert not state
                usage = [line[len(_FULL_USAGE) :].strip()]

            elif line.startswith(_POSITIONAL):
                set_state(_POSITIONAL)

            elif line.startswith(_OPTIONAL):
                set_state(_OPTIONAL)

            elif state is None:
                usage.append(line.strip())

            elif state == _POSITIONAL:
                word, *rest = line.strip().split(maxsplit=1)
                self._argument(word, rest[0] if rest else '')

            else:
                assert state is _OPTIONAL, str(state)
                optionals.append(line)

        if not optionals:
            return

        opt2 = []
        for o in optionals:
            if not opt2 or o.strip().startswith('-'):
                opt2.append(o)
            else:
                opt2[-1] += o

        for i, o in enumerate(opt2):
            if i:
                self._print()

            word, *rest = (i for i in o.strip().split('  ') if i)
            self._argument(word.strip(), ' '.join(rest).strip())

    def _command(self, lines):
        pass

    def _code_block(self, lines):
        self._print('.. code-block:: bash')
        self._print()
        for i, line in enumerate(lines):
            self._print('    ' + line)

    def _usage(self, lines):
        self._print()
        self._header('USAGE')
        self._code_block(lines)

    def _default(self, field, lines):
        self._print()
        self._header(field)
        self._print_lines(lines)

    def _print(self, *args):
        print(*args, file=self.fp)

    def _argument(self, word, rest):
        self._print('  ``%s``: %s' % (word, rest))

    def _header(self, line, underline='='):
        self._print(line)
        self._print(underline * len(line))

    def _print_lines(self, lines):
        if lines:
            self._print()
        for line in lines:
            self._print(line)


_FULL_USAGE = 'Full usage:'
_POSITIONAL = 'positional arguments:'
_OPTIONAL = 'optional arguments:'
