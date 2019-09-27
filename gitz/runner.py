import functools
import itertools
import subprocess

_SUBPROCESS_KWDS = {
    'encoding': 'utf-8',
    'shell': False,
    'stderr': subprocess.PIPE,
    'stdout': subprocess.PIPE,
}
_EXCEPTION_MSG = 'Encountered an exception while executing'


class Runner:
    def __init__(self, log, no_run=False):
        self.log = log
        self.git = Git(self)
        self.no_run = no_run

    def __call__(self, *cmd, quiet=None, silent=None, **kwds):
        quiet = quiet or silent
        self.output_lines, self.error_lines = [], []

        if self.no_run:
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
            self.error_lines.append(line)

        run_proc(proc, out, error)
        if proc.returncode:
            if quiet and not silent:
                for line in self.error_lines:
                    self.log.error('!', line)
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

    @property
    def output_lines(self):
        return self.runner.output_lines

    @property
    def error_lines(self):
        return self.runner.error_lines


def run_proc(pr, out, err):
    def run(fp, callback):
        for i in itertools.count():
            line = fp.readline()
            if not line:
                return i
            callback(line[:-1])

    while run(pr.stdout, out) + run(pr.stderr, err) + (pr.poll() is None):
        pass
