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
SCRIPTED_SVG_DIR = DOC_DIR / 'scripted_movies'
MOVIES_DIR = DOC_DIR / 'movies'

MOVIES_ROOT = ROOT / 'gitz_doc/movies'
CAST_DIR = MOVIES_ROOT / 'recorded'
SCRIPTED_CAST_DIR = DOC_DIR / 'cast'
SCRIPT_DIR = MOVIES_ROOT / 'scripted'

SVG_SUFFIX = '.svg'
CAST_SUFFIX = '.cast'
SCRIPT_SUFFIX = '.sh'

ALL_COMMANDS = 'all-gitz'

HEADER = {'version': 2, 'width': 80, 'height': 32}


def scripted_cast_file(command):
    return (SCRIPTED_CAST_DIR / command).with_suffix(CAST_SUFFIX)


def scripted_svg_file(command):
    return (SCRIPTED_SVG_DIR / command).with_suffix(SVG_SUFFIX)


def movies_file(command):
    return (MOVIES_DIR / command).with_suffix(SVG_SUFFIX)


def script_file(command):
    return (SCRIPT_DIR / command).with_suffix(SCRIPT_SUFFIX)


def cast_files():
    yield from (f for f in CAST_DIR.iterdir() if f.suffix == CAST_SUFFIX)


def script_files():
    yield from (f for f in SCRIPT_DIR.iterdir() if f.suffix == SCRIPT_SUFFIX)
