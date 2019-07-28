from . import log
import functools
import subprocess

_SUBPROCESS_KWDS = {
    'encoding': 'utf-8',
    'shell': True,
    'stderr': subprocess.PIPE,
    'stdout': subprocess.PIPE,
}
_EXCEPTION_MSG = 'Encountered an exception while executing'
add_arguments = log.add_arguments


class GitRunners:
    def __init__(self, program, args):
        main, hidden = log.logs(program, args)
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
            raise ValueError('Git command "%s" failed' % cmd.join(' '))
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
