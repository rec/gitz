from . import command_pages
from . import doc_index
from . import get_command_help
from . import manpages
from . import readme
from .movies import merge
from .movies import recorded_movies
from .movies import scripted_movies
from gitz.program import ARGS
from gitz.program import PROGRAM

SYMBOLS = (
    ('command_pages', command_pages),
    ('doc_index', doc_index),
    ('manpages', manpages),
    ('readme', readme),
    ('scripted_movies', scripted_movies),
    ('recorded_movies', recorded_movies),
    ('merge', merge),
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
