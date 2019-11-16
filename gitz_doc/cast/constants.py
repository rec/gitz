from pathlib import Path

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
