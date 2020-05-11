import sys

_REPLACEMENTS = {
    'git-': 'git ',
    '\npositional arguments:\n': '\nPositional arguments\n',
    '\noptional arguments:\n': '\nOptional arguments\n',
    'usage: ': 'USAGE\n    ',
}


def print_help(program, context, parser):
    if '-h' not in program.argv and '--h' not in program.argv:
        return

    usage = parser.format_help()
    for target, replacement in _REPLACEMENTS.items():
        usage = usage.replace(target, replacement)

    command = program.executable.replace('git-', 'git ', 1)
    fmt = {'command': command, 'usage': usage}
    for f in FIELDS:
        value = context.get(f.upper(), '').lstrip().rstrip()
        if f not in SIMPLE_FIELDS:
            value = _indent(value)
        fmt[f] = value

    if fmt['danger']:
        fmt['danger'] = 'DANGER\n%s%s\n\n' % (INDENT, fmt['danger'])

    if fmt['summary'] and fmt['examples']:
        print(HELP.format(**fmt))
    else:
        print(fmt['usage'].rstrip())
        print(fmt['help'].rstrip())

    sys.exit()


def _indent(text):
    return '\n'.join(INDENT + i for i in text.splitlines()) + '\n'


FIELDS = 'danger', 'examples', 'help', 'image', 'summary'
SIMPLE_FIELDS = 'danger', 'image'
INDENT = '    '

HELP = """\
{command}
{summary}
{usage}
{danger}DESCRIPTION
{help}
EXAMPLES
{examples}"""
