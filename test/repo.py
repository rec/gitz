from tempfile import TemporaryDirectory
import contextlib
import functools
import os
import _gitz

GIT = _gitz.GIT
GIT_SILENT = _gitz.GIT_SILENT

# Generate deterministic commit IDs using fixed data.  See
# https://blog.thoughtram.io/git/2014/11/18/the-anatomy-of-a-git-commit.html

DATE = 'Wed 26 Jun 2019 17:00:05 CEST'
EMAIL = 'unit@test.com'
NAME = 'Unit Test'
ENV_VARIABLES = {
    'GIT_AUTHOR_DATE': DATE,
    'GIT_AUTHOR_EMAIL': EMAIL,
    'GIT_AUTHOR_NAME': NAME,
    'GIT_COMMITTER_DATE': DATE,
    'GIT_COMMITTER_EMAIL': EMAIL,
    'GIT_COMMITTER_NAME': NAME,
}


@contextlib.contextmanager
def contextmanager():
    original_dir = os.getcwd()
    try:
        with TemporaryDirectory() as root:
            os.chdir(root)
            GIT.init()
            none = object()
            original_env = {f: os.environ.get(f, none) for f in ENV_VARIABLES}
            os.environ.update(ENV_VARIABLES)
            try:
                yield root
            finally:
                for f in ENV_VARIABLES:
                    if original_env[f] is none:
                        del os.environ[f]
                    else:
                        os.environ[f] = original_env[f]
    finally:
        os.chdir(original_dir)


@contextlib.contextmanager
def clone(*names):
    clones = []
    with contextlib.ExitStack() as stack:
        for name in names:
            clones.append(stack.enter_context(TemporaryDirectory()))
            GIT.clone('--mirror', '.', clones[-1])
            GIT.remote('add', name, 'file://' + clones[-1])

        yield clones


@contextlib.contextmanager
def environment():
    with contextmanager() as root:
        make_commit('0')
        with clone('origin', 'upstream') as clones:
            yield root, clones


def method(f):
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        with environment():
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
