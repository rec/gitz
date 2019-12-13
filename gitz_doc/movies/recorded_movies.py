from .cast import Cast
from . import constants
from . import keystrokes
from . import render
from . import updater

TIME_SCALE = 0.75


class MovieUpdater(updater.Updater):
    _target = staticmethod(constants.recorded_svg_file)
    _source = staticmethod(constants.recorded_cast_file)

    @classmethod
    def _create(cls, command, target):
        cast = cls._existing(command, target)
        render.render(cast, target)
        return cast

    @classmethod
    def _existing(cls, command, target):
        source = cls._source(command)
        original = Cast.read(source)
        original.replace_prompt()
        cast = keystrokes.fake_text('# ' + source.stem)
        cast.update(original, offset=1)
        cast.remove_exit()
        cast.scale(TIME_SCALE)
        return cast


main = MovieUpdater.update
