from . import constants
from .cast import Cast

ORDERED_COMMANDS = (
    'git-new',
    'git-when',
    'git-st',
    'git-adjust',
    'git-amp',
    'git-copy',
    'git-delete',
    'git-infer',
    'git-rename',
    'git-for-each',
    'git-gitz',
    'git-multi-pick',
    'git-rotate',
    'git-save',
    'git-shuffle',
    'git-split',
    'git-stripe',
    'git-update',
)


def main(commands):
    all_casts = Cast()
    for command in ORDERED_COMMANDS:
        cast_file = constants.command_file(command, 'cast')
        if command not in commands:
            print('Skipping', cast_file)
        elif cast_file.exists():
            cast = Cast.read(cast_file)
            all_casts.update(cast)

    all_casts.write(constants.ALL_COMMANDS_CAST)
    print('wrote', constants.ALL_COMMANDS_CAST)
