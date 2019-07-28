import subprocess

_SUBPROCESS_KWDS = {
    'encoding': 'utf-8',
    'shell': True,
    'stderr': subprocess.PIPE,
    'stdout': subprocess.PIPE,
}
_EXCEPTION_MSG = 'Encountered an exception while executing'


class Runner:
    def __init__(self, log):
        self.log = log

    def run(self, *cmd):
        self.log.command('$', *cmd)
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

    def __call__(self, *cmd):
        returncode, output_lines = self.run(*cmd)
        if returncode:
            raise ValueError('Git command "%s" failed' % cmd.join(' '))
        return output_lines
