import contextlib
import functools
import os
import tempfile
import _gitz

GIT = _gitz.GIT
GIT_SILENT = _gitz.GIT_SILENT
DATE = 'Wed 26 Jun 2019 17:00:05 CEST'
FIELDS = 'GIT_AUTHOR_DATE', 'GIT_COMMITTER_DATE'
AUTHOR = '--author="Unit Test <unit@test.com>"'


@contextlib.contextmanager
def contextmanager():
    original_dir = os.getcwd()
    try:
        with tempfile.TemporaryDirectory() as root:
            os.chdir(root)
            GIT.init()
            none = object()
            original = {f: os.environ.get(f, none) for f in FIELDS}
            os.environ.update((f, DATE) for f in FIELDS)
            try:
                yield
            finally:
                for f in FIELDS:
                    if original[f] is none:
                        del os.environ[f]
                    else:
                        os.environ[f] = original[f]
    finally:
        os.chdir(original_dir)


def method(f):
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        with contextmanager():
            f(*args, **kwds)

    return wrapper


def make_commit(*names):
    for n in names:
        with open(n, 'w') as fp:
            fp.write(n)
            fp.write('\n')
        GIT.add(n)
    name = '_'.join(names)
    GIT.commit('-m', name, AUTHOR)
    return GIT.commit_id()[: _gitz.COMMIT_ID_LENGTH]
