from . import constants
from . import render
from . import script_runner
from . import updater
from .cast import Cast
from test import repo

ALL = 'all-gitz'
COMMITS = 'one', 'two', 'three', 'four', 'five'


class ScriptedUpdater(updater.Updater):
    def __init__(self, command):
        self.target = constants.scripted_svg_file(command)
        self.source = constants.script_file(command)
        self.cast_file = constants.scripted_cast_file(command)

    def _create(self):
        with repo.clone_context():
            cast = script_runner.run(self.source)
            _render(cast, self.cast_file, self.target)
            return cast

    def _existing(self):
        return Cast.read(self.cast_file)


@repo.sandbox()
def main(commands):
    results = ScriptedUpdater.update(commands)
    all_casts = Cast()
    for symbol, cast in results:
        all_casts.update(cast)

    all_cast_file = constants.scripted_cast_file(ALL)
    target_file = constants.scripted_svg_file(ALL)
    _render(all_casts, all_cast_file, target_file)
    print('wrote', ALL)


def _render(cast, cast_file, target):
    cast.write(cast_file)
    render.render(cast, target)
