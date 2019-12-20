from .cast import Cast
from . import constants


def main(commands):
    all_casts = Cast()

    for command in commands:
        cast_file = constants.command_file(command, 'cast')
        if cast_file.exists():
            cast = Cast.read(cast_file)
            all_casts.update(cast)

    all_casts.write(constants.ALL_COMMANDS_CAST)
    print('wrote', constants.ALL_COMMANDS_CAST)
