from . import log
from . import runner
from pathlib import Path
import argparse
import sys
import traceback

_ERROR_PROTECTED_BRANCHES = 'The branches %s are protected'


class _Program:
    def __init__(self):
        self.code = -1
        self.executable = Path(sys.argv[0]).name
        self.argv = sys.argv[1:]
        self.called = {}

    def run(self, USAGE='', HELP='', add_arguments=None, **kwds):
        self.initialize(USAGE, HELP, add_arguments)
        exe = self.executable.replace('-', '_')
        main = kwds.get(exe) or kwds.get('main')
        if not main:
            self.exit('No method named', exe, 'or main in', self.executable)

        try:
            main()

        except Exception as e:
            self.log.verbose(traceback.format_exc(), file=sys.stderr)
            self.exit('%s: %s' % (e.__class__.__name__, e))

    def initialize(self, usage, help, add_arguments=None):
        self.usage = usage
        self.help = help
        if self._print_help():
            print()
            print('Full ', end='')

        parser = argparse.ArgumentParser()
        log.add_arguments(parser)
        add_arguments and add_arguments(parser)

        # If -h/--help are set, this next call terminates the program
        self.args = parser.parse_args(self.argv)
        self.log = log.Log(self.args)
        self.run = runner.Runner(self.log)
        self.git = self.run.git
        return self.args

    def check_help(self):
        """If help requested, print it and exit"""
        if self._print_help():
            sys.exit(0)

    def exit(self, *messages):
        if messages:
            self.error(*messages)
        sys.exit(self.code)

    def error(self, *messages):
        self._error(messages, 'error')

    def warning(self, *messages):
        self._error(messages, 'warning')

    def message(self, *messages):
        self.log.message(*messages)

    def _error(self, messages, category):
        caption = self.executable + ':'
        self.called[category] = True
        caption = category.upper() + ':' + caption
        self.log.error(caption, *messages, file=sys.stderr)

    def _print_help(self):
        if '-h' in self.argv or '--h' in self.argv:
            print(self.usage.rstrip())
            print(self.help.rstrip())
            return True


PROGRAM = _Program()
