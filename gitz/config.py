from pathlib import Path
import sys

VERSION = '0.9.11'
LIBRARY_DIRECTORY = Path(__file__).absolute().parent
EXECUTABLE_DIRECTORY = Path(sys.argv[0]).absolute().parent


def _commands():
    def commands(d):
        return [f.name for f in d.iterdir() if f.name.startswith('git-')]

    return sorted(
        commands(LIBRARY_DIRECTORY.parent) or commands(EXECUTABLE_DIRECTORY)
    )


COMMANDS = _commands()
