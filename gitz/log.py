from enum import IntEnum

FLAGS = {
    'silent': 'Suppress all output',
    'quiet': 'Only output errors and warnings',
    'verbose': 'Report all messages in great detail',
}


class Level(IntEnum):
    SILENT = 0
    QUIET = 1
    USEFUL = 2
    VERBOSE = 3


def add_arguments(parser):
    add = parser.add_argument
    for flag, help in FLAGS.items():
        add('-' + flag[0], '--' + flag, action='store_true', help=help)


def log_level(args=None):
    if args is None:
        return Level.USEFUL
    if (args.verbose + args.quiet + args.silent) > 1:
        pass  # Can't really deal with this here?
    if args.verbose:
        return Level.VERBOSE
    if args.quiet:
        return Level.QUIET
    if args.silent:
        return Level.SILENT
    return Level.USEFUL
