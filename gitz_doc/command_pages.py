from . import dirs
from .movies import constants
from gitz.git import functions

_HOME_LINK = '`Gitz home page <https://github.com/rec/gitz/>`_'
SECTIONS = (
    'TITLE',
    'USAGE',
    'Positional arguments',
    'Optional arguments',
    'DESCRIPTION',
    'DANGER',
    'MOVIE',
    'EXAMPLES',
)

# If USE_BRANCH_NAME is True, the current branchname is
# used for svg files, otherwise master is always used.
USE_BRANCH_NAME = False


def main(commands):
    for command, help in commands.items():
        help_file = (dirs.DOC / command).with_suffix('.rst')
        with open(help_file, 'w') as fp:
            Writer(help, fp).write()


class Writer:
    def __init__(self, sections, fp):
        self.command = sections['COMMAND'].replace('git-', 'git ')
        self.sections = sections
        self.fp = fp

    def write(self):
        self.sections['TITLE'] = self.sections[self.command]

        for section_name in SECTIONS:
            lines = self.sections.get(section_name)
            if lines or section_name == 'MOVIE':
                name = '_' + section_name.split()[0].lower()
                method = getattr(self, name, self._default)
                method(section_name, lines)

    def _default(self, field, lines):
        self._print()
        self._block(field, lines)

    def _title(self, name, lines):
        title = '``%s``: %s' % (self.command, lines[0])
        self._block(title, lines[1:], '-')

    def _usage(self, name, lines):
        self._header(name)
        self._print('.. code-block:: bash')
        self._print()
        for line in lines:
            self._print('    ' + line)

    def _positional(self, name, lines):
        self._print()
        self._print(name)
        for line in lines:
            word, *rest = line.strip().split(maxsplit=1)
            self._argument(word, rest[0] if rest else '')

    def _optional(self, name, lines):
        self._print()
        self._print(name)
        optionals = []
        for line in lines:
            if not optionals or line.strip().startswith('-'):
                optionals.append(line)
            else:
                optionals[-1] += line

        for i, o in enumerate(optionals):
            if i:
                self._print()

            word, *rest = (i for i in o.strip().split('  ') if i)
            self._argument(word.strip(), ' '.join(rest).strip())

    def _movie(self, name, lines):
        cmd = self.command.replace('git ', 'git-')
        image_file = constants.command_file(cmd, 'svg')
        if not image_file.exists():
            return
        self._print()
        self._header(name)
        branch = functions.branch_name()
        self._print(_IMAGE_SECTION.format(command=cmd, branch=branch))

    def _examples(self, name, lines):
        self._print()
        self._header(name)
        for line in lines:
            if not line:
                self._print()
            elif line.startswith(' '):
                self._print(line)
            else:
                self._print('``%s``' % line)

    def _print(self, *args):
        print(*args, file=self.fp)

    def _argument(self, word, rest):
        self._print('  ``%s``: %s' % (word, rest))

    def _block(self, line, lines, underline='='):
        self._header(line, underline)
        self._print_lines(lines)

    def _header(self, line, underline='='):
        self._print(line)
        self._print(underline * len(line))
        self._print()

    def _print_lines(self, lines):
        for line in lines:
            self._print(line)


_FULL_USAGE = 'USAGE'
_POSITIONAL = 'Positional arguments'
_OPTIONAL = 'Optional arguments'
_IMAGE_SECTION = """\
.. figure:: https://raw.githubusercontent.com/rec/gitz/{branch}/doc/movies/\
{command}.svg?sanitize=true
    :align: center
    :alt: {command}.svg\
"""
