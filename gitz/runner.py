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
    def __init__(self, log):
        self.log = log
        self.git = Git(self)

    def __call__(self, *cmd, **kwds):
        self.log.verbose('$', *cmd)
        kwds = dict(_SUBPROCESS_KWDS, **kwds)
        if kwds.get('shell'):
            cmd = ' '.join(cmd)
        proc = subprocess.Popen(cmd, **kwds)
        output_lines = []

        def out(line):
            self.log.verbose(line[:-1])
            output_lines.append(line[:-1])

        def error(line):
            self.log.error(line[:-1])

        while proc.poll() is None or run_proc(proc, out, error):
            pass

        if proc.returncode:
            raise ValueError('Command "%s" failed' % ' '.join(cmd))

        return output_lines


class Git:
    def __init__(self, run):
        self.run = run

    def __getattr__(self, command):
        return functools.partial(self.run, 'git', command)

    def __call__(self, *cmd):
        return self.run('git', *cmd)


def run_proc(proc, out, error):
    running = True
    while running:
        running = False

        while True:
            line = proc.stdout.readline()
            if not line:
                break
            out(line)
            running = True

        while True:
            line = proc.stderr.readline()
            if not line:
                break
            error(line)
            running = True

        if proc.poll() is None:
            running = True
