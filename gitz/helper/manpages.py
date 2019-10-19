from . import dirs
import io


# Taken from rst2man.py
from docutils.core import publish_file, default_description
from docutils.writers import manpage

DESCRIPTION = ('Generates unix manual pages for gitz. ' + default_description)
HEADINGS = 'Positional arguments', 'Optional arguments'


def main(commands):
    for command in commands:
        src = (dirs.DOC / command).with_suffix('.rst')
        dest = (dirs.MAN / command).with_suffix('.1')
        contents = fix_rst(src)

        publish_file(
            writer=manpage.Writer(),
            source=io.StringIO(contents),
            source_path=str(src),
            destination=dest.open('w'),
        )


def fix_rst(src):
    lines = []
    in_examples = False
    examples = []

    def pop_example_stack():
        for example in examples[1:]:
            lines.extend((example, '    (same)', ''))
        examples.clear()

    for line in src.open():
        line = line[:-1]
        lines.append(line)
        if line in HEADINGS:
            lines.append('=' * len(line))
        elif not in_examples:
            in_examples = (line == 'EXAMPLES')
        elif line.startswith('`'):
            if examples:
                lines.pop()
            examples.append(line)
        elif not line.strip():
            pop_example_stack()
    if examples[1:]:
        lines.append('')
    pop_example_stack()

    return '\n'.join(lines) + '\n'
