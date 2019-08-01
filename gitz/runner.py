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

    def __call__(self, *cmd):
        self.log.command(*cmd)
        proc = subprocess.Popen(cmd, **_SUBPROCESS_KWDS)
        output_lines = []

        def read_io():
            stdout = proc.stdout.readline()
            if stdout:
                self.log.stdout(stdout[:-1])
                output_lines.append(stdout[:-1])

            stderr = proc.stderr.readline()
            if stderr:
                self.log.stderr(stderr[:-1])

            return stdout or stderr

        while proc.poll() is None or read_io():
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
