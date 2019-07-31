from gitz import git
from gitz import git_functions
from gitz.git import GIT
from gitz.program import Program
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
        with _with_tmpdir(), _with_env_variables(**ENV_VARIABLES):
            GIT.init()
            make_commit('0')
            with clone(*DEFAULT_ORIGINS):
                with _with_attr(self, 'program', Program('Usage!', 'Help!')):
                    f(self)

    return wrapper


@contextlib.contextmanager
def clone(*names):
    clones = []
    with contextlib.ExitStack() as stack:
        for name in names:
            clones.append(stack.enter_context(TemporaryDirectory()))
            GIT.clone('--mirror', '.', clones[-1])
            GIT.remote('add', name, 'file://' + clones[-1])
            GIT.fetch(name)

        yield clones


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
    return git_functions.commit_id()[: git.COMMIT_ID_LENGTH]


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
