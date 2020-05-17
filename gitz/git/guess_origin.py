from . import functions
from ..program import ENV


def guess_origin(origin=None, branch=None):
    if origin:
        if origin in functions.remote_branches(False):
            return origin
        raise ValueError('Unknown remote %s' % origin)
    try:
        return functions.upstream_remote(branch)
    except Exception:
        pass

    try:
        rb = functions.remote_branches(False)
        return next(o for o in ENV.origin() if o in rb)
    except Exception:
        raise ValueError('Cannot determine origin')
