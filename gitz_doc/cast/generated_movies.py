from . import constants
from . import script_runner
from .cast import Cast
from test import repo
ALL = 'all-gitz'


@repo.sandbox('one', 'two', 'three', 'four', 'five')
def main(commands):
    all_casts = Cast()

    for command in commands:
        script_file = constants.script_file(command)
        if not script_file.exists():
            continue

        ts = script_file.stat().st_mtime
        cast_file = constants.generated_cast_file(command)
        if cast_file.exists() and cast_file.stat().st_mtime >= ts:
            print('=', cast_file)
            continue

        cast = script_runner.run(script_file)
        cast.write(cast_file)
        print('+', cast_file)
        all_casts.merge(cast)

    all_casts.write(constants.generated_cast_file(ALL))
    print('wrote', ALL)
