from pathlib import Path
import sys

__version__ = '1.1.3'
HOME_PAGE = 'https://github.com/rec/gitz/blob/master/README.rst'

# In development and when running tests, LIBRARY_DIRECTORY and
# EXECUTABLE_DIRECTORY will be the same but in a pip installation
# they will be different!
LIBRARY_DIRECTORY = Path(__file__).absolute().parent.parent
EXECUTABLE_DIRECTORY = Path(sys.argv[0]).absolute().parent

# These commands are not ready for primetime and so distributed with gitz
EXPERIMENTAL_COMMANDS = 'git-for-each', 'git-save'


def _commands():
    def commands(d):
        if not d.exists():
            return []
        return [f.name for f in d.iterdir() if f.name.startswith('git-')]

    cmds = commands(LIBRARY_DIRECTORY) or commands(EXECUTABLE_DIRECTORY)
    return sorted(c for c in cmds if c not in EXPERIMENTAL_COMMANDS)


COMMANDS = _commands()
