import subprocess

_SUBPROCESS_KWDS = {
    'encoding': 'utf-8',
    'shell': False,
    'stderr': subprocess.PIPE,
    'stdout': subprocess.PIPE,
}


def run_proc(cmd, kwds, out, err):
    """Run a subprocess with error and output callbacks"""
    kwds = dict(_SUBPROCESS_KWDS, **kwds)
    if kwds.get('shell'):
        cmd = ' '.join(cmd)

    p = subprocess.Popen(cmd, **kwds)

    def run(fp, callback):
        line = fp.readline()
        if not line:
            return False
        while line:
            callback(line[:-1])
            line = fp.readline()
        return True

    while run(p.stdout, out) or run(p.stderr, err) or (p.poll() is None):
        pass

    if p.returncode:
        raise ValueError('Command "%s" failed' % ' '.join(cmd))
