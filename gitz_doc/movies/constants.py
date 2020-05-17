from . import colors
from pathlib import Path

PROMPT = '▶ {BLUE}tom{RED}:{GREEN}/code/test{NONE}$ '
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

HEADER = {'version': 2, 'width': 100, 'height': 40}

MAX_KEYSTROKE_TIME = 0.7
KEYSTROKE_TIME_SCALE = 0.32
TIME_TO_THINK = 1
TIME_AT_END = 5
TIME_TO_READ_ONE_CHAR = 0.005
TYPING_ERROR_RATE = 0.06


def command_file(command, name):
    dirname = FILES[name]
    return (dirname / command).with_suffix('.' + name)


def recorded_cast_files():
    yield from (f for f in CAST_DIR.iterdir() if f.suffix == '.cast')


ALL_COMMANDS_CAST = command_file(ALL_COMMANDS, 'cast')
ALL_COMMANDS_JSON = ALL_COMMANDS_CAST.with_suffix('.json')
