from . import constants
from . import needs_update
from . import render
from . import script_runner
from .cast import Cast
from test import repo

ALL = 'all-gitz'
COMMITS = 'one', 'two', 'three', 'four', 'five'


class GeneratedUpdater(needs_update.Updater):
    _target = staticmethod(constants.generated_svg_file)
    _source = staticmethod(constants.script_file)

    @classmethod
    def _create(cls, target, source):
        with repo.clone_context():
            cast = script_runner.run(source)
            render.render(cast, target)
            return cast

    @classmethod
    def _existing(cls, target, source):
        return Cast.read(target)


@repo.sandbox()
def main(commands):
    results = GeneratedUpdater.update(commands)
    all_casts = Cast()
    for symbol, cast in results:
        all_casts.update(cast)

    all_casts.write(constants.generated_cast_file(ALL))
    print('wrote', ALL)
