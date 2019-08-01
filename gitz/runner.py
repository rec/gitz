import functools
import subprocess

_SUBPROCESS_KWDS = {
    'encoding': 'utf-8',
    'shell': False,
    'stderr': subprocess.PIPE,
    'stdout': subprocess.PIPE,
}
_EXCEPTION_MSG = 'Encountered an exception while executing'


class GitRunners:
    def __init__(self, main, hidden):
        self.main = GitRunner(main)
        self.hidden = GitRunner(hidden)

    def __getattr__(self, command):
        return getattr(self.main, command)

    def __call__(self, *cmd):
        return self.main.git(*cmd)


class GitRunner:
    def __init__(self, log):
        self.log = log

    def __getattr__(self, command):
        return functools.partial(self.git, command)

    def git(self, *cmd):
        return self('git', *cmd)

    def __call__(self, *cmd):
        returncode, output_lines = self.run(*cmd)
        if returncode:
            raise ValueError('Command "%s" failed' % ' '.join(cmd))
        return output_lines

    def run(self, *cmd):
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

        while proc.poll() is None:
            read_io()

        read_io()
        return proc.returncode, output_lines
