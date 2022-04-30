import shlex
import subprocess

_SUBPROCESS_KWDS = {
    'shell': False,
    'stderr': subprocess.PIPE,
    'stdout': subprocess.PIPE,
}


class RunProcError(ValueError):
    pass




def run_proc(cmd, out=None, err=None, **kwds):
    """Run a subprocess with separate error and output callbacks"""
    out = [] if out is None else out
    err = err or out
    kwds = dict(_SUBPROCESS_KWDS, **kwds)
    if kwds.get('shell'):
        if not isinstance(cmd, str):
            cmd = ' '.join(cmd)

    elif isinstance(cmd, str):
        cmd = shlex.split(cmd)

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
        o = out if callable(out) else out.append
        e = err if callable(err) else err.append

        while run(p.stdout, o) or run(p.stderr, e) or p.poll() is None:
            pass

    if p.returncode:
        raise RunProcError('Command "%s" failed' % ' '.join(cmd))

    return out
