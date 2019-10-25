from . import run_proc
import functools


class Runner:
    def start(self, log, no_run=False):
        self.log = log
        self.no_run = no_run

    def __call__(self, *cmd, quiet=None, merged=False, info=False, **kwds):
        """
        quiet: If True, no output is printed
        merged: If True, error data is merged into the output
        info: If False, do not execute the command in dry run mode
              If True, always execute the command, even in dry run mode
        """
        if self.no_run and not info:
            self.log.message('$', *cmd)
            return []

        errors, output, merge = [], [], []

        def out(line):
            if not quiet:
                self.log.verbose('>', line)
            output.append(line)
            merge.append(('>', line))

        def err(line):
            if not quiet:
                self.log.error('!', line)
            errors.append(line)
            merge.append(('!', line))

        self.log.verbose('$', *cmd)
        try:
            run_proc.run_proc(cmd, kwds, out, err)
        except Exception:
            if quiet:
                for symbol, line in merged:
                    self.log.error(symbol, line)
            raise

        return [line for _, line in merge] if merged else output


class Git:
    def __init__(self, runner):
        self.runner = runner

    def __getattr__(self, command):
        return functools.partial(self, command.replace('_', '-'))

    def __call__(self, *cmd, **kwds):
        return self.runner('git', *cmd, **kwds)


RUN = Runner()
GIT = Git(RUN)
