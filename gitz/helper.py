class Helper:
    def __init__(self, command, **kwds):
        self.command = command
        for f in FIELDS:
            setattr(self, f, kwds.get(f.upper(), ''))
        self.usage = self._indent(self.usage)
        self.examples = self._indent(self.examples)
        if self.danger:
            self.danger = 'DANGER: %s\n' % self.danger

    def print_help(self):
        if self.summary and self.examples:
            print(HELP.format(**vars(self)).rstrip())
        else:
            print(self.usage.rstrip())
            print(self.help.rstrip())

    INDENT = '  '

    def _indent(self, text):
        return '\n'.join(self.INDENT + i for i in text.splitlines()) + '\n'


FIELDS = 'danger', 'examples', 'help', 'summary', 'usage'

HELP = """\
{command}: {summary}

USAGE:
{usage}
{danger}{help}
EXAMPLES:
{examples}
"""
