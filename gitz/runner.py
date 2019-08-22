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
    def __init__(self, log, dry_run=False):
        self.log = log
        self.git = Git(self)
        self.dry_run = dry_run

    def __call__(self, *cmd, **kwds):
        if self.dry_run:
            self.log.message('$', *cmd)
            return []

        self.log.verbose('$', *cmd)
        kwds = dict(_SUBPROCESS_KWDS, **kwds)
        cmd_arg = ' '.join(cmd)
        if kwds.get('shell'):
            cmd = cmd_arg

        proc = subprocess.Popen(cmd, **kwds)
        self.output_lines = []

        run_proc(proc, self._out, self._error)
        if proc.returncode:
            raise ValueError('Command "%s" failed' % cmd_arg)

        return self.output_lines

    def _out(self, line):
        self.log.verbose(line[:-1])
        self.output_lines.append(line[:-1])

    def _error(self, line):
        self.log.error(line[:-1])


class Git:
    def __init__(self, run):
        self.run = run

    def __getattr__(self, command):
        return functools.partial(self, command)

    def __call__(self, *cmd, **kwds):
        if cmd[0] == 'git':
            raise ValueError

        return self.run('git', *cmd, **kwds)


def run_proc(pr, out, err):
    def run(fp, callback):
        for i in itertools.count():
            line = fp.readline()
            if not line:
                return i
            callback(line)

    while run(pr.stdout, out) + run(pr.stderr, err) + (pr.poll() is None):
        pass
