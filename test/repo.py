from gitz import git_functions
from gitz.program import PROGRAM
from gitz.program import git
from tempfile import TemporaryDirectory
import contextlib
import functools
import os

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
DEFAULT_ORIGINS = 'origin', 'upstream'


def test(f):
    @functools.wraps(f)
    def wrapper(self):
        PROGRAM.argv.clear()
        PROGRAM.initialize()
        with _with_tmpdir(), _with_env_variables(**ENV_VARIABLES):
            git.init()
            make_commit('0')
            with clone(*DEFAULT_ORIGINS):
                with _with_attr(self, 'program', PROGRAM):
                    f(self)

    return wrapper


@contextlib.contextmanager
def clone(*names):
    clones = []
    with contextlib.ExitStack() as stack:
        for name in names:
            clones.append(stack.enter_context(TemporaryDirectory()))
            git.clone('--mirror', '.', clones[-1])
            git.remote('add', name, 'file://' + clones[-1])
            git_functions.fetch(name)

        yield clones


def write_file(name, contents):
    with open(name, 'w') as fp:
        fp.write(contents)


def write_files(*names, **kwds):
    for name in names:
        write_file(name, name + '\n')

    for name, contents in kwds.items():
        write_file(name, contents)


def add_files(*names):
    for name in names:
        git.add(name)


def make_commit(*names, **kwds):
    write_files(*names, **kwds)
    add_files(*names)
    add_files(*kwds)
    return commit('_'.join(names + tuple(kwds)))


def commit(message):
    git.commit('-m', message)
    return git_functions.commit_id()[: git_functions.COMMIT_ID_LENGTH]


def make_one_commit(filename, contents, message):
    write_file(filename, contents)
    add_files(filename)
    return commit(message)


@contextlib.contextmanager
def _with_tmpdir():
    with TemporaryDirectory() as root:
        original_dir = os.getcwd()
        os.chdir(root)
        try:
            yield root
        finally:
            os.chdir(original_dir)


@contextlib.contextmanager
def _with_env_variables(**variables):
    original_env = {f: os.environ.get(f) for f in variables}
    os.environ.update(variables)
    try:
        yield
    finally:
        for f in variables:
            if original_env[f] is None:
                del os.environ[f]
            else:
                os.environ[f] = original_env[f]


@contextlib.contextmanager
def _with_attr(item, attr, value):
    none = object()
    original_value = getattr(item, attr, none)
    setattr(item, attr, value)
    try:
        yield item
    finally:
        if original_value is none:
            delattr(item, attr)
        else:
            setattr(item, attr, original_value)
