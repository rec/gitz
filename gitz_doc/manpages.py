from . import clean_manpage
from . import dirs
from gitz import config
import datetime
import safer


def main(commands):
    date = format(datetime.datetime.now(), '%d %B, %Y')

    for command, sections in commands.items():
        Manpage(command, sections, date).write()


class Manpage:
    def __init__(self, command, sections, date):
        self.command = command
        self.sections = clean_manpage.clean_sections(sections)
        self.date = date
        self.COMMAND = command.upper()
        self.description = sections[command.replace('-', ' ', 1)][0]
        self.usage = sections['USAGE'][0]
        self.version = config.__version__

    def write(self):
        manfile = (dirs.MAN / self.command).with_suffix('.1')
        with safer.writer(manfile) as self.fp:
            self._print(HEADER.format(**vars(self)))
            for field in FIELDS:
                if field in self.sections:
                    self._write_field(field)

    def _write_field(self, field):
        if field != POSITIONAL:
            if field == OPTIONAL:
                self._print('.SH OPTIONS')
            else:
                self._print('.SH', field.upper())
        attrname = '_' + field.lower().split()[0]
        method = getattr(self, attrname, self._section)
        method(self.sections[field])
        self._print()

    def _positional(self, lines):
        for line in lines:
            word, *rest = line.strip().split(maxsplit=1)
            self._argument(word, rest[0] if rest else '')

    def _optional(self, lines):
        optionals = []
        for line in lines:
            if not optionals or line.strip().startswith(r'\-'):
                optionals.append(line)
            else:
                optionals[-1] += line

        for i, o in enumerate(optionals):
            word, *rest = (i for i in o.strip().split('  ') if i)
            self._argument(word.strip(), ' '.join(rest).strip())

    def _examples(self, lines):
        for line in lines:
            if not line:
                self._print()
                self._print('.sp')
            elif line.startswith(' '):
                self._print(line.strip())
            else:
                self._print('.TP')
                self._print('.B', clean_manpage.START, line, clean_manpage.END)

    def _section(self, lines):
        for line in lines:
            self._print(line)
            if not line:
                self._print('.sp')

    def _print(self, *args, **kwds):
        print(*args, file=self.fp, **kwds)

    def _argument(self, word, rest):
        self._print(
            r'%s%s%s: %s'
            % (clean_manpage.START, word, clean_manpage.END, rest)
        )
        self._print()


HEADER = """\
.TH {COMMAND} 1 "{date}" "Gitz {version}" "Gitz Manual"

.SH NAME
{command} - {description}

.SH SYNOPSIS
.sp
.nf
.ft C
{usage}
.ft P
.fi

"""

POSITIONAL = 'Positional arguments'
OPTIONAL = 'Optional arguments'

FIELDS = ('DESCRIPTION', OPTIONAL, POSITIONAL, 'DANGER', 'EXAMPLES')
