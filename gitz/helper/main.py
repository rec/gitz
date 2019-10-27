from . import directory
from . import manpages
from . import reader
from . import rsts
from . import summary
from ..program import PROGRAM


def main():
    help = reader.read()
    directory.main(help)
    rsts.main(help)
    summary.main(help)
    manpages.main(help)


if __name__ == '__main__':
    PROGRAM.start()
    main()
