from . import command
from . import reader
from . import summary
from ..program import PROGRAM


def full_main():
    commands = reader.read()
    summary.main(commands)
    command.main(commands)


def main():
    import json
    print(json.dumps(reader.read(), indent=4))
    print(reader.read().keys())


if __name__ == '__main__':
    PROGRAM.initialize()
    full_main()
