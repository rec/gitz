FLAGS = {
    'silent': 'Suppress all output',
    'quiet': 'Only output errors and warnings',
    'verbose': 'Report all messages in great detail',
}


def add_arguments(parser):
    add = parser.add_argument
    for flag, help in FLAGS.items():
        add('-' + flag[0], '--' + flag, action='store_true', help=help)


def logs(program, args):
    if (args.verbose + args.quiet + args.silent) > 1:
        program.warning(
            'Only one of --verbose, --quiet and --silent should be set'
        )

    log, hidden = _Log.Useful, _Log.Silent

    if args.verbose:
        log = hidden = _Log.Verbose
    elif args.silent:
        log = _Log.Silent
    elif args.quiet:
        log = _Log.Quiet

    return log(program), hidden(program)


class _Log:
    class Silent:
        def __init__(self, program):
            self.program = program

        def command(self, *cmd):
            pass

        def stdout(self, line):
            pass

        def stderr(self, line):
            pass

    class Quiet(Silent):
        def stderr(self, line):
            self.program.error('?', line)

    class Useful(Quiet):
        def command(self, *cmd):
            self.program.info('$', *cmd)

    class Verbose(Useful):
        def stdout(self, line):
            self.program.info(line)
