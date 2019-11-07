from pathlib import Path

FILE = Path(__file__)
ROOT = FILE.parent.parent

SVG_DIR = ROOT / 'doc' / 'movies'
SVG_SUFFIX = '.svg'

CAST_DIR = ROOT / 'cast'
CAST_SUFFIX = '.cast'

TEMPLATE = 'dracula'


def main(commands):
    def _time(f):
        return f.exists() and f.stat().st_mtime

    SVG_DIR.mkdir(exist_ok=True, parents=True)

    for command in commands:
        cast_file = (CAST_DIR / command).with_suffix(CAST_SUFFIX)
        if cast_file.exists():
            svg_file = (SVG_DIR / command).with_suffix(SVG_SUFFIX)
            if _time(svg_file) < max(_time(cast_file), _time(FILE)):
                _render(str(cast_file), str(svg_file))


def _render(cast_file, svg_file):
    from termtosvg.main import (
        DEFAULT_LOOP_DELAY,
        render_subcommand,
    )  # , logger
    from termtosvg.config import default_templates

    render_subcommand(
        still=False,
        template=default_templates()[TEMPLATE],
        cast_filename=cast_file,
        output_path=svg_file,
        min_frame_duration=1,
        max_frame_duration=None,
        loop_delay=DEFAULT_LOOP_DELAY,
    )

    print('+', svg_file)
