from . import constants
from . import script_runner
from . import updater
from .cast import Cast
from test import repo

COMMITS = 'one', 'two', 'three', 'four', 'five'


class ScriptedUpdater(updater.Updater):
    ALL_CASTS = constants.scripted_cast_file(constants.ALL_COMMANDS)
    ALL_SVG = constants.scripted_svg_file(constants.ALL_COMMANDS)

    def __init__(self, command):
        self.target = constants.scripted_svg_file(command)
        self.source = constants.script_file(command)
        self.cast_file = constants.scripted_cast_file(command)

    def _create(self):
        with repo.clone_context():
            cast = script_runner.run(self.source)
            self.render(cast, self.cast_file, self.target)
            return cast

    def _existing(self):
        return Cast.read(self.cast_file)


@repo.sandbox()
def main(commands):
    ScriptedUpdater.update(commands)
