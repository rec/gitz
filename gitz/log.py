import functools
import sys

FLAGS = {
    'silent': 'Suppress all output',
    'quiet': 'Only output errors and warnings',
    'verbose': 'Report all messages in great detail',
}


def add_arguments(parser):
    add = parser.add_argument
    for flag, help in FLAGS.items():
        add('-' + flag[0], '--' + flag, action='store_true', help=help)


def Log(args):
    error = functools.partial(print, file=sys.stderr)

    if (args.verbose + args.quiet + args.silent) > 1:
        error('WARNING: Only set one of --verbose, --quiet or --silent')

    if args.silent:
        return _Log()

    if args.quiet:
        return _Log(error=error)

    if not args.verbose:
        return _Log(error=error, message=print)

    return _Log(error=error, message=print, verbose=print)


def _nothing(*args):
    pass


class _Log:
    def __init__(self, error=_nothing, message=_nothing, verbose=_nothing):
        self.error = error
        self.message = message
        self.verbose = verbose
