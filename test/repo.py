from gitz.git import functions
from gitz.program import PROGRAM
from gitz.git import GIT
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
        def main():
            with _with_tmpdir(), _with_env_variables(**ENV_VARIABLES):
                GIT.init()
                make_commit('0')
                with clone(*DEFAULT_ORIGINS):
                    with _with_attr(self, 'program', PROGRAM):
                        f(self)

        PROGRAM.argv.clear()
        PROGRAM.start({'main': main})

    return wrapper


@contextlib.contextmanager
def clone(*names):
    clones = []
    with contextlib.ExitStack() as stack:
        for name in names:
            clones.append(stack.enter_context(TemporaryDirectory()))
            GIT.clone('--mirror', '.', clones[-1])
            GIT.remote('add', name, 'file://' + clones[-1])
            functions.fetch(name)

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
        GIT.add(name)


def make_commit(*names, **kwds):
    write_files(*names, **kwds)
    add_files(*names)
    add_files(*kwds)
    return commit('_'.join(names + tuple(kwds)))


def commit(message):
    GIT.commit('-m', message)
    return functions.commit_id()


def make_one_commit(filename, contents, message):
    write_file(filename, contents)
    add_files(filename)
    return commit(message)


def make_seven_commits(testcase):
    testcase.assertEqual(GIT.log('--oneline'), ['c0d1dbb 0'])

    make_commit('1')
    make_commit('2')
    make_commit('3')
    make_commit('4')
    make_commit('5')
    make_commit('6')
    make_commit('7')

    actual = GIT.log('--oneline')
    expected = [
        'e487041 7',
        'e1e931a 6',
        '8a4a4e2 5',
        'a7c7e8f 4',
        '9ab30c5 3',
        '043df1f 2',
        'a03c0f8 1',
        'c0d1dbb 0',
    ]
    testcase.assertEqual(actual, expected)


@contextlib.contextmanager
def _with_tmpdir():
    with TemporaryDirectory() as td:
        original_dir = os.getcwd()
        os.chdir(td)
        try:
            yield td
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
