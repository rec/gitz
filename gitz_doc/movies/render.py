from pathlib import Path
from termtosvg import anim
from termtosvg import asciicast
from termtosvg import config
from termtosvg import term
import tempfile

TEMPLATE = 'solarized_light'


def render(cast, svg_file):
    with tempfile.TemporaryDirectory() as td:
        cast_file = Path(td) / 'file.cast'
        cast.write(cast_file)
        _render_file(cast_file, svg_file)


def _render_file(cast_file, svg_file):
    asciicast_records = asciicast.read_records(str(cast_file))
    geometry, frames = term.timed_frames(asciicast_records)

    template = config.default_templates()[TEMPLATE]
    anim.render_animation(frames, geometry, str(svg_file), template)
