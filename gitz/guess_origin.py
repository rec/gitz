from .env import ENV
from .program import safe_git
from . import git_functions


def upstream_remote(branch=None):
    # https://stackoverflow.com/a/9753364/43839
    upstream = 'rev-parse --abbrev-ref --symbolic-full-name %s@{u}'
    cmd = (upstream % (branch or '')).split()
    lines = safe_git(*cmd, silent=True)
    return lines[0].split('/', maxsplit=1)[0]


def guess_origin(origin=None, branch=None):
    if origin:
        if origin in git_functions.remote_branches(False):
            return origin
        raise ValueError('Unknown remote %s' % origin)
    try:
        return upstream_remote(branch)
    except Exception:
        pass

    try:
        rb = git_functions.remote_branches(False)
        return next(o for o in ENV.origin() if o in rb)
    except Exception:
        raise ValueError('Cannot determine origin')
