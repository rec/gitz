from . import command
from . import reader
from . import summary
from ..program import PROGRAM


def main():
    commands = reader.read()
    command.main(commands)
    summary.main(commands)


if __name__ == '__main__':
    PROGRAM.initialize()
    main()
