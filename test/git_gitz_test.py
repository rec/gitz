from . import repo
from gitz import config
from gitz.runner import GIT
import unittest


class GitGitzTest(unittest.TestCase):
    maxDiff = 100000

    @repo.test
    def test_all(self):
        self.assertEqual(GIT.gitz(), RESULTS)

    @repo.test
    def test_version(self):
        for v in 'v', 've', 'version':
            self.assertEqual(GIT.gitz(v), [config.VERSION])

    @repo.test
    def test_commands(self):
        expected = COMMANDS
        for c in 'c', 'com', 'commands':
            self.assertEqual(GIT.gitz(c), expected)

    @repo.test
    def test_executable_directory(self):
        # The configs for the child process and for us are different!
        for d in 'e', 'exec', 'executable_directory':
            self.assertEqual(
                GIT.gitz(d), [str(config.LIBRARY_DIRECTORY.parent)]
            )

    @repo.test
    def test_library_directory(self):
        for d in 'l', 'lib', 'library_directory':
            self.assertEqual(GIT.gitz(d), [str(config.LIBRARY_DIRECTORY)])

    @repo.test
    def test_defaults(self):
        for d in 'd', 'def', 'defaults':
            self.assertEqual(GIT.gitz(d), DEFAULTS)

    @repo.test
    def test_error(self):
        with self.assertRaises(ValueError):
            GIT.gitz('var')

        with self.assertRaises(ValueError):
            GIT.gitz('Com')


HOME_PAGE = config.HOME_PAGE
EXECUTABLE_DIRECTORY = str(config.LIBRARY_DIRECTORY.parent)
LIBRARY_DIRECTORY = str(config.LIBRARY_DIRECTORY)
VERSION = config.VERSION
COMMANDS = """\
git-all:
    Perform a command on each of multiple branches or directories
git-amp:
    AMend the last commit message and force-Push, somewhat safely
git-copy:
    Copy a git branch locally and on all remotes
git-delete:
    Delete one or more branches locally and on all remotes

git-gitz:
    Print information about the gitz environment
git-infer:
    Commit changes with an auto-generated message
git-multi-pick:
    Cherry-pick multiple commits, with an optional squash
git-new:
    Create and push new branches

git-rename:
    Rename a git branch locally and on all remotes
git-rotate:
    Rotate the current branch forward or backward in the list of branches
git-shuffle:
    Reorder and delete commits in the current branch
git-split:
    Split a range of commits into many single-file commits

git-st:
    Colorful, compact git status
git-stripe:
    Push a sequence of commit IDs to a remote repository
git-update:
    Update branches from a reference branch
git-when:
    When did each file change (date, commit, message)?
""".splitlines()

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
