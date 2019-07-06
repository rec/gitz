import contextlib
import functools
import os
import tempfile
import _gitz

GIT = _gitz.GIT
GIT_SILENT = _gitz.GIT_SILENT
DATE = 'Wed 26 Jun 2019 17:00:05 CEST'
NAME = 'Unit Test'
EMAIL = 'unit@test.com'
FIELDS = {
    'GIT_AUTHOR_DATE': DATE,
    'GIT_COMMITTER_DATE': DATE,
    'GIT_COMMITTER_NAME': NAME,
    'GIT_COMMITTER_EMAIL': EMAIL,
    'GIT_AUTHOR_NAME': NAME,
    'GIT_AUTHOR_EMAIL': EMAIL,
}


@contextlib.contextmanager
def contextmanager():
    original_dir = os.getcwd()
    try:
        with tempfile.TemporaryDirectory() as root:
            os.chdir(root)
            GIT.init()
            none = object()
            original = {f: os.environ.get(f, none) for f in FIELDS}
            os.environ.update(FIELDS)
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


def write_files(*names):
    for name in names:
        with open(name, 'w') as fp:
            fp.write(name)
            fp.write('\n')


def add_files(*names):
    for name in names:
        GIT.add(name)


def make_commit(*names):
    write_files(*names)
    add_files(*names)
    GIT.commit('-m', '_'.join(names))
    return GIT.commit_id()[: _gitz.COMMIT_ID_LENGTH]
