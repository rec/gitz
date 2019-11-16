from pathlib import Path
from termtosvg import config
from termtosvg import main as ts_main
from . import constants

TEMPLATE = 'base16_default_dark'
LAST_MODIFIED = max(f.stat().st_mtime for f in Path(__file__).parent.iterdir())
RENDER = {
    'still': False,
    'min_frame_duration': 1,
    'max_frame_duration': None,
    'loop_delay': ts_main.DEFAULT_LOOP_DELAY,
}


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

    ts_main.render_subcommand(
        template=config.default_templates()[TEMPLATE],
        cast_filename=str(cast_file),
        output_path=str(svg_file),
        **RENDER)
    return '+'
