from .cast import Cast
from . import constants
from . import keystrokes
from . import render
from . import updater

TIME_SCALE = 0.75


class MovieUpdater(updater.Updater):
    ALL_CASTS = constants.recorded_cast_file(constants.ALL_COMMANDS)
    ALL_SVG = constants.recorded_svg_file(constants.ALL_COMMANDS)

    def __init__(self, command):
        self.target = constants.recorded_svg_file(command)
        self.source = constants.recorded_cast_file(command)

    def _create(self):
        cast = self._existing()
        render.render(cast, self.target)
        return cast

    def _existing(self):
        original = Cast.read(self.source)
        original.replace_prompt()
        cast = keystrokes.fake_text('# ' + self.source.stem)
        cast.update(original, offset=1)
        cast.remove_exit()
        cast.scale(TIME_SCALE)
        return cast


main = MovieUpdater.update
