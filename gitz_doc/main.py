from . import command_pages
from . import doc_index
from . import get_command_help
from . import manpages
from . import readme
from .cast import movies
from gitz.program import ARGS
from gitz.program import PROGRAM

SYMBOLS = (
    ('doc_index', doc_index),
    ('command_pages', command_pages),
    ('readme', readme),
    ('manpages', manpages),
    ('movies', movies),
)


def add_arguments(parser):
    parser.add_argument('sections', nargs='*', help='Sections')


def main():
    help = get_command_help.get_command_help()
    sections = ARGS.sections
    for s, module in SYMBOLS:
        if not sections or any(s.startswith(i) for i in sections):
            module.main(help)
            print(s, 'done')


if __name__ == '__main__':
    PROGRAM.start()
