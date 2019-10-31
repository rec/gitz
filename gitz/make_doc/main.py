from . import command_pages
from . import doc_index
from . import manpages
from . import get_command_help
from . import readme
from ..program import PROGRAM


def main():
    help = get_command_help.get_command_help()
    doc_index.main(help)
    command_pages.main(help)
    readme.main(help)
    manpages.main(help)


if __name__ == '__main__':
    PROGRAM.start()
    main()
