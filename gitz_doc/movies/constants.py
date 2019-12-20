from pathlib import Path
from . import colors

PROMPT = '{LIGHT_RED}tom{NONE}@host{BLUE}:{GREEN}/code/test{NONE}$ '
PROMPT = PROMPT.format(**vars(colors))

BACKSPACE = '\x08\x1b[K'
RETURN = '\r\n'
CONTROL_L = '\x1b[H\x1b[2J'

FILE = Path(__file__)
ROOT = FILE.parents[2]

DOC_DIR = ROOT / 'doc'

MOVIES_ROOT = ROOT / 'gitz_doc/movies'
CAST_DIR = MOVIES_ROOT / 'recorded'

FILES = {
    'svg': DOC_DIR / 'movies',
    'cast': DOC_DIR / 'cast',
    'sh': MOVIES_ROOT / 'scripted',
}

ALL_COMMANDS = 'all-gitz'

HEADER = {'version': 2, 'width': 80, 'height': 32}


def command_file(command, name):
    dirname = FILES[name]
    return (dirname / command).with_suffix('.' + name)


def recorded_cast_files():
    yield from (f for f in CAST_DIR.iterdir() if f.suffix == '.cast')


ALL_COMMANDS_CAST = command_file(ALL_COMMANDS, 'cast')
