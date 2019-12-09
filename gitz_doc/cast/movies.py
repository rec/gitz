from . import cast
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
        result = cls._existing(target, source)
        render.render(result, target)
        return result

    @classmethod
    def _existing(cls, target, source):
        original = cast.Cast.read(source)
        original.replace_prompt()
        result = keystrokes.fake_text('# ' + source.stem)
        result.update(original, offset=1)
        result.remove_exit()
        result.scale(TIME_SCALE)
        return result


main = MovieUpdater.update
