from . import log
from . import print_help
import argparse

_NO_RUN_HELP = 'If set, commands will be printed but not executed'


def parse(program, add_arguments=None, **context):
    parser = argparse.ArgumentParser(formatter_class=HelpFormatter)
    log.add_arguments(parser)
    add_arguments and add_arguments(parser)
    if program.ALLOW_NO_RUN:
        parser.add_argument(
            '-n', '--no-run', action='store_true', help=_NO_RUN_HELP
        )

    # If -h or --help are set, this next call terminates the program
    print_help.print_help(program, context, parser)
    args = parser.parse_args(program.argv)
    return args, log.Log(args)


class HelpFormatter(argparse.HelpFormatter):
    def __init__(
        self, prog, indent_increment=4, max_help_position=16, width=None
    ):
        super().__init__(prog, indent_increment, max_help_position, width)
