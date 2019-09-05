def helper(program, context):
    if not ('-h' in program.argv or '--h' in program.argv):
        return False

    fmt = {'command': program.executable}
    for f in FIELDS:
        value = context.get(f.upper(), '').lstrip().rstrip()
        if f not in SIMPLE_FIELDS:
            value = _indent(value)
        fmt[f] = value

    if fmt['danger']:
        fmt['danger'] = 'DANGER:\n%s%s\n\n' % (INDENT, fmt['danger'])

    if fmt['summary'] and fmt['examples']:
        print(HELP.format(**fmt).rstrip())
    else:
        print(fmt['usage'].rstrip())
        print(fmt['help'].rstrip())

    print('\n---\n')
    print('Full ', end='')
    return True


def _indent(text):
    return '\n'.join(INDENT + i for i in text.splitlines()) + '\n'


FIELDS = 'danger', 'examples', 'help', 'image', 'summary', 'usage'
SIMPLE_FIELDS = 'danger', 'image'
INDENT = '    '

HELP = """\
{command}:
{summary}
USAGE:
{usage}
{danger}DESCRIPTION:
{help}
EXAMPLES:
{examples}
"""
