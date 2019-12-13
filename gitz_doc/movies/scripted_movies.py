from . import constants
from . import render
from . import script_runner
from . import updater
from .cast import Cast
from test import repo

ALL = 'all-gitz'
COMMITS = 'one', 'two', 'three', 'four', 'five'


class ScriptedUpdater(updater.Updater):
    _target = staticmethod(constants.scripted_svg_file)
    _source = staticmethod(constants.script_file)

    @classmethod
    def _create(cls, command, target):
        with repo.clone_context():
            source = cls._source(command)
            cast = script_runner.run(source)
            render.render(cast, target)
            return cast

    @classmethod
    def _existing(cls, command, target):
        return Cast.read(constants.scripted_cast_file(command))


@repo.sandbox()
def main(commands):
    results = ScriptedUpdater.update(commands)
    all_casts = Cast()
    for symbol, cast in results:
        all_casts.update(cast)

    all_casts.write(constants.scripted_cast_file(ALL))
    print('wrote', ALL)
