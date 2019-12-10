from .cast import Cast
from . import constants
from . import keystrokes
from . import needs_update
from . import render

TIME_SCALE = 0.75


class MovieUpdater(needs_update.Updater):
    _target = staticmethod(constants.svg_file)
    _source = staticmethod(constants.cast_file)

    @classmethod
    def _create(cls, target, source):
        cast = cls._existing(target, source)
        render.render(cast, target)
        return cast

    @classmethod
    def _existing(cls, target, source):
        original = Cast.read(source)
        original.replace_prompt()
        cast = keystrokes.fake_text('# ' + source.stem)
        cast.update(original, offset=1)
        cast.remove_exit()
        cast.scale(TIME_SCALE)
        return cast


main = MovieUpdater.update
