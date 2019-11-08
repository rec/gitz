from . import repo
from gitz import config
from gitz.git import GIT
from gitz.program import summaries
import platform
import unittest


class GitGitzTest(unittest.TestCase):
    maxDiff = 100000

    @repo.test
    def test_all(self):
        # See #170
        expected = [r for r in RESULTS if not r.startswith('    Python')]
        actual = [r for r in GIT.gitz('-v') if not r.startswith('    Python')]
        self.assertEqual(expected, actual)

    @repo.test
    def test_version(self):
        for v in 'v', 've', 'version':
            self.assertEqual(GIT.gitz(v, '-v'), [config.VERSION])

    @repo.test
    def test_commands(self):
        expected = COMMANDS
        for c in 'c', 'com', 'commands':
            actual = GIT.gitz(c, '-v')
            self.assertEqual(actual, expected)
            self.assertEqual(len(actual), len(expected))

    @repo.test
    def test_executable_directory(self):
        # The configs for the child process and for us are different!
        for d in 'e', 'exec', 'executable_directory':
            self.assertEqual(
                GIT.gitz(d, '-v'), [str(config.LIBRARY_DIRECTORY.parent)]
            )

    @repo.test
    def test_library_directory(self):
        for d in 'l', 'lib', 'library_directory':
            self.assertEqual(
                GIT.gitz(d, '-v'), [str(config.LIBRARY_DIRECTORY)]
            )

    @repo.test
    def test_defaults(self):
        for d in 'd', 'def', 'defaults':
            self.assertEqual(GIT.gitz(d, '-v'), DEFAULTS)

    @repo.test
    def test_error(self):
        with self.assertRaises(ValueError):
            GIT.gitz('var', '-v')

        with self.assertRaises(ValueError):
            GIT.gitz('Com', '-v')


def _commands():
    for i, (cmd, summary) in enumerate(sorted(summaries.SUMMARIES.items())):
        if i and not (i % 4):
            yield ''

        yield cmd + ':'
        yield '    ' + summary


HOME_PAGE = config.HOME_PAGE
EXECUTABLE_DIRECTORY = str(config.LIBRARY_DIRECTORY.parent)
LIBRARY_DIRECTORY = str(config.LIBRARY_DIRECTORY)
VERSION = config.VERSION
PYTHON_VERSION = platform.python_version()
PLATFORM = platform.platform()

COMMANDS = list(_commands())
INDENT_COMMANDS = '\n'.join(('    ' if c else '') + c for c in COMMANDS)

RESULTS = """\
Commands:
{INDENT_COMMANDS}

Defaults:
    GITZ_ORIGIN = ['origin']
    GITZ_PROTECTED_BRANCHES = ['develop', 'master', 'release']
    GITZ_PROTECTED_REMOTES = ['upstream']
    GITZ_REFERENCE_BRANCHES = ['develop', 'master']
    GITZ_UPSTREAM = ['upstream', 'origin']

Executable directory:
    {EXECUTABLE_DIRECTORY}

Home page:
    {HOME_PAGE}

Library directory:
    {LIBRARY_DIRECTORY}

Python:
    Python v{PYTHON_VERSION} on {PLATFORM}

Version:
    {VERSION}
""".format(
    **globals()
).splitlines()

DEFAULTS = """\
GITZ_ORIGIN = ['origin']
GITZ_PROTECTED_BRANCHES = ['develop', 'master', 'release']
GITZ_PROTECTED_REMOTES = ['upstream']
GITZ_REFERENCE_BRANCHES = ['develop', 'master']
GITZ_UPSTREAM = ['upstream', 'origin']
""".splitlines()
