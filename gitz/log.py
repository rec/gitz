import functools
import sys

FLAGS = {
    'quiet': 'Suppress all output',
    'verbose': 'Report all messages in great detail',
}


def add_arguments(parser):
    add = parser.add_argument
    for flag, help in FLAGS.items():
        add('-' + flag[0], '--' + flag, action='store_true', help=help)


def Log(args):
    error = functools.partial(print, file=sys.stderr)

    if args.verbose and args.quiet:
        error('WARNING: Only one of --verbose or --quiet may be set')

    if args.quiet:
        return _Log(flush=_nothing)

    if not args.verbose:
        return _Log(error=error, message=print)

    return _Log(error=error, message=print, verbose=print)


def _nothing(*args, **kwds):
    pass


class _Log:
    def __init__(
        self,
        error=_nothing,
        message=_nothing,
        verbose=_nothing,
        flush=sys.stdout.flush,
    ):
        self.error = error
        self.message = message
        self.verbose = verbose
        self.flush = flush
