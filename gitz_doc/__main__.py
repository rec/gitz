from . import command_pages
from . import doc_index
from . import get_command_help
from . import manpages
from . import readme
from .movies import all_movies
from .movies import movies
from gitz import config
from gitz.program import ARGS
from gitz.program import PROGRAM

SYMBOLS = (
    ('command_pages', command_pages),
    ('doc_index', doc_index),
    ('manpages', manpages),
    ('movies', movies),
    ('all_movies', all_movies),
    ('readme', readme),
)


def add_arguments(parser):
    parser.add_argument('sections', nargs='*', help='Sections')


def main():
    help = get_command_help.get_command_help(config.COMMANDS)
    sections = ARGS.sections
    for s, module in SYMBOLS:
        if not sections or any(s.startswith(i) for i in sections):
            module.main(help)
            print(s, 'done')


if __name__ == '__main__':
    PROGRAM.start()
