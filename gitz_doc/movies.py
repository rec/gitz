from pathlib import Path
from termtosvg import config
from termtosvg import main as ts_main

FILE = Path(__file__)
ROOT = FILE.parent.parent

SVG_DIR = ROOT / 'doc' / 'movies'
CAST_DIR = ROOT / 'cast'

SVG_SUFFIX = '.svg'
CAST_SUFFIX = '.cast'

TEMPLATE = 'base16_default_dark'


def main(commands):
    def _time(f):
        return f.exists() and f.stat().st_mtime

    SVG_DIR.mkdir(exist_ok=True, parents=True)

    for command in commands:
        cast_file = (CAST_DIR / command).with_suffix(CAST_SUFFIX)
        if cast_file.exists():
            svg_file = (SVG_DIR / command).with_suffix(SVG_SUFFIX)
            if _time(svg_file) < max(_time(cast_file), _time(FILE)):
                _render(cast_file, svg_file)


def _render(cast_file, svg_file):
    template = config.default_templates()[TEMPLATE]

    ts_main.render_subcommand(
        still=False,
        template=template,
        cast_filename=str(cast_file),
        output_path=str(svg_file),
        min_frame_duration=1,
        max_frame_duration=None,
        loop_delay=ts_main.DEFAULT_LOOP_DELAY,
    )

    print('+', svg_file)
