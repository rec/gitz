from .helper import helper
from . import log
from . import runner
from pathlib import Path
import argparse
import collections
import sys
import traceback

_ERROR_PROTECTED_BRANCHES = 'The branches %s are protected'
_NO_RUN_HELP = 'If set, commands will be printed but not executed'


class _Program:
    ALLOW_NO_RUN = True

    def __init__(self):
        self.code = -1
        self.executable = Path(sys.argv[0]).name
        self.argv = sys.argv[1:]
        self.called = collections.Counter()

    def initialize(self, add_arguments=None, **kwds):
        self.helper = helper.Helper(self.executable, **kwds)
        if self.helper.print_help(self.argv):
            print('\n---\n')
            print('Full ', end='')

        parser = argparse.ArgumentParser()
        log.add_arguments(parser)
        add_arguments and add_arguments(parser)
        if self.ALLOW_NO_RUN:
            parser.add_argument(
                '-n', '--no-run', action='store_true', help=_NO_RUN_HELP
            )

        # If -h/--help are set, this next call terminates the program
        self.args = parser.parse_args(self.argv)
        self.log = log.Log(self.args)
        self._safe_run = runner.Runner(self.log)
        if self.ALLOW_NO_RUN and self.args.no_run:
            self._run = runner.Runner(self.log, no_run=True)
        else:
            self._run = self._safe_run

        self._quiet_run = runner.Runner(self.log, quiet=True)
        return self.args

    def start(self, add_arguments=None, **kwds):
        self.initialize(add_arguments, **kwds)
        exe = self.executable.replace('-', '_')
        main = kwds.get(exe) or kwds.get('main')
        if not main:
            self.exit('No method named', exe, 'or main in', self.executable)

        try:
            main()

        except Exception as e:
            self.log.verbose(traceback.format_exc(), file=sys.stderr)
            self.exit('%s: %s' % (e.__class__.__name__, e))

    def safe_run(self, *command, **kwds):
        return self._run(*command, **kwds)

    def quiet_run(self, *command, **kwds):
        return self._quiet_run(*command, **kwds)

    def run(self, *command, **kwds):
        return self._run(*command, **kwds)

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
        self.called[category] += 1
        caption = category.upper() + ':' + caption
        self.log.error(caption, *messages, file=sys.stderr)


PROGRAM = _Program()

safe_run = PROGRAM.safe_run
safe_git = runner.Git(safe_run)

run = PROGRAM.run
git = runner.Git(run)

quiet_run = PROGRAM.run
quiet_git = runner.Git(run)
