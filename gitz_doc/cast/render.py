from termtosvg import config
from termtosvg import main

TEMPLATE = 'base16_default_dark'
RENDER = {
    'still': False,
    'min_frame_duration': 1,
    'max_frame_duration': None,
    'loop_delay': main.DEFAULT_LOOP_DELAY,
}


def render(cast_file, svg_file):
    main.render_subcommand(
        template=config.default_templates()[TEMPLATE],
        cast_filename=str(cast_file),
        output_path=str(svg_file),
        **RENDER)
