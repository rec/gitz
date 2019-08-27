from . import command
from . import reader
from . import summary
from ..program import PROGRAM


def main():
    PROGRAM.initialize()
    commands = reader.read()
    summary.main(commands)
    command.main(commands)


if __name__ == '__main__':
    main()
