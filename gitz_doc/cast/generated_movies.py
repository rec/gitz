from . import constants
from . import needs_update
from . import script_runner
from .cast import Cast
from test import repo
ALL = 'all-gitz'


@repo.sandbox('one', 'two', 'three', 'four', 'five')
def main(commands):
    all_casts = Cast()

    for command in commands:
        script_file = constants.script_file(command)
        cast_file = constants.generated_cast_file(command)
        update = needs_update.needs_update(cast_file, script_file)
        if update == '?':
            print(update, script_file)
        else:
            if update == '.':
                cast = Cast.read(cast_file)
            else:
                cast = script_runner.run(script_file)
            all_casts.merge(cast)
            print(update, cast_file)

    all_casts.write(constants.generated_cast_file(ALL))
    print('wrote', ALL)
