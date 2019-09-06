from . import parser
from . import runner
from pathlib import Path
import collections
import sys
import traceback

_ERROR_PROTECTED_BRANCHES = 'The branches %s are protected'


class _Program:
    ALLOW_NO_RUN = True

    def __init__(self):
        self.code = -1
        self.executable = Path(sys.argv[0]).name
        self.argv = sys.argv[1:]
        self.called = collections.Counter()

    def start(self, context=None):
        if context is None:
            context = vars(sys.modules['__main__'])
        self.initialize(**context)
        exe = self.executable.replace('-', '_')
        main = context.get(exe) or context.get('main')
        if not main:
            self.exit('No method named', exe, 'or main in', self.executable)

        try:
            main()

        except Exception as e:
            self.log.verbose(traceback.format_exc(), file=sys.stderr)
            self.exit('%s: %s' % (e.__class__.__name__, e))

    def initialize(self, **context):
        self.args, self.log = parser.parse(self, **context)
        self._safe_run = runner.Runner(self.log)
        if self.ALLOW_NO_RUN and self.args.no_run:
            self._run = runner.Runner(self.log, no_run=True)
        else:
            self._run = self._safe_run

        self._quiet_run = runner.Runner(self.log, quiet=True)
        return self.args

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
