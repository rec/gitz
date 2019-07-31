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
        while proc.poll() is None:
            stdout = proc.stdout.readline()
            if stdout:
                self.log.stdout(stdout)
                output_lines.append(stdout)

            stderr = proc.stderr.readline()
            if stderr:
                self.log.stderr(stderr)

        return proc.returncode, output_lines
