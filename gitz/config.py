from pathlib import Path
import sys

VERSION = '0.9.12'
LIBRARY_DIRECTORY = Path(__file__).absolute().parent
EXECUTABLE_DIRECTORY = Path(sys.argv[0]).absolute().parent
HOME_PAGE = 'https://github.com/rec/gitz/blob/master/README.rst'


def _commands():
    def commands(d):
        return [f.name for f in d.iterdir() if f.name.startswith('git-')]

    return sorted(
        commands(LIBRARY_DIRECTORY.parent) or commands(EXECUTABLE_DIRECTORY)
    )


COMMANDS = _commands()
