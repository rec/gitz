
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

    if args.verbose:
        return _Log.Verbose(program), _Log.Verbose(program)

    if args.silent:
        return _Log.Silent(program), _Log.Silent(program)

    if args.quiet:
        return _Log.Quiet(program), _Log.Silent(program)

    return _Log.Useful(program), _Log.Silent(program)


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
            self.program.error(line)

    class Useful(Quiet):
        def command(self, *cmd):
            self.program.info('$', *cmd)

    class Verbose(Useful):
        def stdout(self, line):
            self.program.info(line)
