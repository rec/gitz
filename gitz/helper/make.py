from . import command
from . import directory
from . import reader
from . import summary
from ..program import PROGRAM


def main():
    help = reader.read()
    directory.main(help)
    command.main(help)
    summary.main(help)


if __name__ == '__main__':
    PROGRAM.initialize()
    main()
