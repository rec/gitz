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
    def __init__(self, log, quiet=None, no_run=False):
        self.log = log
        self.git = Git(self)
        self.no_run = no_run
        self.quiet = quiet

    def __call__(self, *cmd, quiet=None, **kwds):
        if quiet is None:
            quiet = self.quiet
        if self.no_run:
            self.log.message('$', *cmd)
            return []

        self.log.verbose('$', *cmd)
        kwds = dict(_SUBPROCESS_KWDS, **kwds)
        cmd_arg = ' '.join(cmd)
        if kwds.get('shell'):
            cmd = cmd_arg

        proc = subprocess.Popen(cmd, **kwds)
        output_lines = []

        def out(line):
            if not quiet:
                self.log.verbose(line[:-1])
            output_lines.append(line[:-1])

        def error(line):
            if not quiet:
                self.log.error(line[:-1])

        run_proc(proc, out, error)
        if proc.returncode:
            raise ValueError('Command "%s" failed' % cmd_arg)

        return output_lines


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
