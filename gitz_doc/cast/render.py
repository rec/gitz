from termtosvg import asciicast
from termtosvg import anim
from termtosvg import config
from termtosvg import term

TEMPLATE = 'base16_default_dark'


def render(cast_file, svg_file):
    template = config.default_templates()[TEMPLATE]

    asciicast_records = asciicast.read_records(str(cast_file))
    geometry, frames = term.timed_frames(asciicast_records)
    anim.render_animation(frames, geometry, str(svg_file), template)
