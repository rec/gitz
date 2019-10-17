import functools

from . import run_proc


class Runner:
    def start(self, log, no_run=False):
        self.log = log
        self.no_run = no_run

    def __call__(self, *cmd, quiet=None, merged=False, info=False, **kwds):
        """
        quiet: If True, no output is printed
        merged: If True, error data is merged into the output
        info: If info is False, do not execute the command in dry run mode.
              If info is True, always execute this command.
        """

        if self.no_run and not info:
            self.log.message('$', *cmd)
            return []

        output_lines = []

        def out(line):
            if not quiet:
                self.log.verbose('>', line)
            output_lines.append(line)

        def error(line):
            if not quiet:
                self.log.error('!', line)
            if merged:
                output_lines.append(line)

        self.log.verbose('$', *cmd)
        run_proc.run_proc(cmd, kwds, out, error)

        return output_lines


class Git:
    def __init__(self, runner):
        self.runner = runner

    def __getattr__(self, command):
        return functools.partial(self, command)

    def __call__(self, *cmd, **kwds):
        return self.runner('git', *cmd, **kwds)


RUN = Runner()
GIT = Git(RUN)
