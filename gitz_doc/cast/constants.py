from pathlib import Path

BACKSPACE = '\x08\x1b[K'
RETURN = '\r\n'
CONTROL_L = '\x1b[H\x1b[2J'

FILE = Path(__file__)
ROOT = FILE.parents[2]

SVG_DIR = ROOT / 'doc' / 'movies'
CAST_DIR = ROOT / 'cast'

SVG_SUFFIX = '.svg'
CAST_SUFFIX = '.cast'


def cast_file(command):
    return (CAST_DIR / command).with_suffix(CAST_SUFFIX)


def svg_file(command):
    return (SVG_DIR / command).with_suffix(SVG_SUFFIX)


def cast_files():
    yield from (f for f in CAST_DIR.iterdir() if f.suffix == CAST_SUFFIX)
