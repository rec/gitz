import subprocess

_SUBPROCESS_KWDS = {
    'shell': False,
    'stderr': subprocess.PIPE,
    'stdout': subprocess.PIPE,
}


def run_proc(cmd, kwds, out, err):
    """Run a subprocess with error and output callbacks"""
    kwds = dict(_SUBPROCESS_KWDS, **kwds)
    if kwds.get('shell'):
        cmd = ' '.join(cmd)

    def run(fp, callback):
        line = fp.readline()
        if not line:
            return False
        while line:
            s = line.decode('utf-8')
            callback(s.rstrip('\n'))
            line = fp.readline()
        return True

    with subprocess.Popen(cmd, **kwds) as p:
        while run(p.stdout, out) or run(p.stderr, err) or (p.poll() is None):
            pass

    if p.returncode:
        raise ValueError('Command "%s" failed' % ' '.join(cmd))
