import functools
import subprocess

_SUBPROCESS_KWDS = {
    'encoding': 'utf-8',
    'shell': False,
    'stderr': subprocess.PIPE,
    'stdout': subprocess.PIPE,
}
_EXCEPTION_MSG = 'Encountered an exception while executing'


class Runner:
    def start(self, log, no_run=False):
        self.git = Git(self)
        self.log = log
        self.no_run = no_run

    def __call__(self, *cmd, quiet=None, merged=False, info=False, **kwds):
        """
        quiet: If True, no output is printed
        merged: If True, error data is merged into the output
        info: If info is False, do not execute the command in dry run mode.
              If info is True, always execute this command.
        """
        self.output_lines = []

        if self.no_run and not info:
            self.log.message('$', *cmd)
            return []

        self.log.verbose('$', *cmd)
        kwds = dict(_SUBPROCESS_KWDS, **kwds)
        if kwds.get('shell'):
            cmd = ' '.join(cmd)

        proc = subprocess.Popen(cmd, **kwds)

        def out(line):
            if not quiet:
                self.log.verbose('>', line)
            self.output_lines.append(line)

        def error(line):
            if not quiet:
                self.log.error('!', line)
            if merged:
                self.output_lines.append(line)

        run_proc(proc, out, error)
        if proc.returncode:
            raise ValueError('Command "%s" failed' % ' '.join(cmd))

        return self.output_lines


class Git:
    def __init__(self, runner):
        self.runner = runner

    def __getattr__(self, command):
        return functools.partial(self, command)

    def __call__(self, *cmd, **kwds):
        if cmd[0] == 'git':
            raise ValueError

        return self.runner('git', *cmd, **kwds)


RUN = Runner()
RUN_INFO = Runner()
GIT = Git(RUN)
GIT_INFO = Git(RUN_INFO)


def run_proc(pr, out, err):
    def run(fp, callback):
        line = fp.readline()
        if not line:
            return False
        while line:
            callback(line[:-1])
            line = fp.readline()
        return True

    while run(pr.stdout, out) or run(pr.stderr, err) or (pr.poll() is None):
        pass
