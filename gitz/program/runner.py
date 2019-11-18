from . import run_proc
import functools

OUT = '>'
ERR = '!'


class Runner:
    def start(self, log, no_run=False):
        self.log = log
        self.no_run = no_run

    def __call__(self, *cmd, quiet=True, merged=False, info=False, **kwds):
        """
        quiet: If True, no output is printed unless an exception is thrown
        merged: If True, error data is merged into the output
        info: If False, do not execute the command in dry run mode
              If True, always execute the command, even in dry run mode
        """
        if self.no_run and not info:
            self.log.message('$', *cmd)
            return []

        items = []
        error_log = self.log.verbose if quiet else self.log.error

        def out(line):
            self.log.verbose(OUT, line)
            items.append((OUT, line))

        def err(line):
            error_log(ERR, line)
            items.append((ERR, line))

        self.log.verbose('$', *cmd)
        try:
            run_proc.run_proc(cmd, out, err, **kwds)
        except Exception as e:
            e._runner_output = items
            raise

        accept = (OUT + ERR) if merged else OUT
        return [line for (symbol, line) in items if symbol in accept]


class Git:
    def __init__(self, runner):
        self.runner = runner

    def __getattr__(self, command):
        return functools.partial(self, command.replace('_', '-'))

    def __call__(self, *cmd, **kwds):
        return self.runner('git', *cmd, **kwds)


RUN = Runner()
GIT = Git(RUN)
