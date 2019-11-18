from pathlib import Path
from . import cast
from . import constants
from . import keystrokes
from . import render
import tempfile

TEMPLATE = 'base16_default_dark'
LAST_MODIFIED = max(f.stat().st_mtime for f in Path(__file__).parent.iterdir())
PROMPT = '/code/sandbox$ '
TIME_SCALE = 0.75


def main(commands):
    constants.SVG_DIR.mkdir(exist_ok=True, parents=True)
    for command in commands:
        print(command, _one_file(command))


def _one_file(command):
    cast_file = constants.cast_file(command)
    if not cast_file.exists():
        return '?'

    svg_file = constants.svg_file(command)
    if svg_file.exists() and svg_file.stat().st_mtime >= LAST_MODIFIED:
        return '.'

    original = cast.Cast.read(cast_file)
    original.replace_prompt(PROMPT)

    result = keystrokes.fake_text('# ' + cast_file.stem, PROMPT)
    result.merge(original, offset=1)
    result.remove_exit()
    result.scale(TIME_SCALE)

    with tempfile.TemporaryDirectory() as td:
        temp_file = Path(td) / 'file.cast'
        result.write(temp_file)
        render.render(temp_file, svg_file)
    return '+'
