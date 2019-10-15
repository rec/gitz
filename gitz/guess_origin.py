from .env import ENV
from . import git_functions


def guess_origin(origin=None, branch=None):
    if origin:
        if origin in git_functions.remote_branches(False):
            return origin
        raise ValueError('Unknown remote %s' % origin)
    try:
        return git_functions.upstream_remote(branch)
    except Exception:
        pass

    try:
        rb = git_functions.remote_branches(False)
        return next(o for o in ENV.origin() if o in rb)
    except Exception:
        raise ValueError('Cannot determine origin')
