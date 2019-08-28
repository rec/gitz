from . import repo
from gitz import config
from gitz.program import safe_git
import unittest


class GitGitzTest(unittest.TestCase):
    @repo.test
    def test_all(self):
        self.assertEqual(safe_git.gitz(), RESULTS)

    @repo.test
    def test_version(self):
        for v in 'v', 've', 'version':
            self.assertEqual(safe_git.gitz(v), [config.VERSION])

    @repo.test
    def test_commands(self):
        for c in 'c', 'com', 'commands':
            self.assertEqual(safe_git.gitz(c), list(config.COMMANDS))

    @repo.test
    def test_directory(self):
        for d in 'dir', 'directory':
            self.assertEqual(safe_git.gitz(d), [str(config.ROOT_DIR)])

    @repo.test
    def test_defaults(self):
        for d in 'd', 'def', 'defaults':
            self.assertEqual(safe_git.gitz(d), DEFAULTS)

    @repo.test
    def test_error(self):
        with self.assertRaises(ValueError):
            safe_git.gitz('var')

        with self.assertRaises(ValueError):
            safe_git.gitz('Com')


VERSION = config.VERSION
ROOT_DIR = str(config.ROOT_DIR)

RESULTS = """\
Commands:
  git-all
  git-amp
  git-combine
  git-copy
  git-delete
  git-fresh
  git-gitz
  git-infer
  git-ls
  git-rename
  git-rotate
  git-shuffle
  git-snip
  git-split
  git-st
  git-stripe

Defaults:
  GITZ_ORIGIN = ['origin']
  GITZ_PROTECTED_BRANCHES = ['develop', 'master']
  GITZ_PROTECTED_REMOTES = ['upstream']
  GITZ_REFERENCE_BRANCHES = ['develop', 'master']
  GITZ_UPSTREAM = ['upstream', 'origin']

Directory:
  {ROOT_DIR}

Version:
  {VERSION}
""".format(
    **globals()
).splitlines()

DEFAULTS = """\
GITZ_ORIGIN = ['origin']
GITZ_PROTECTED_BRANCHES = ['develop', 'master']
GITZ_PROTECTED_REMOTES = ['upstream']
GITZ_REFERENCE_BRANCHES = ['develop', 'master']
GITZ_UPSTREAM = ['upstream', 'origin']
""".splitlines()
