from . import repo
from gitz.program import git
from setup import COMMANDS
from setup import ROOT_DIR
from setup import VERSION
import unittest


class GitGitzTest(unittest.TestCase):
    @repo.test
    def test_all(self):
        self.assertEqual(git.gitz(), RESULTS)

    @repo.test
    def test_version(self):
        for v in 'v', 've', 'version':
            self.assertEqual(git.gitz(v), [VERSION])

    @repo.test
    def test_commands(self):
        for c in 'c', 'com', 'commands':
            self.assertEqual(git.gitz(c), list(COMMANDS))

    @repo.test
    def test_directory(self):
        for d in 'dir', 'directory':
            self.assertEqual(git.gitz(d), [ROOT_DIR])

    @repo.test
    def test_defaults(self):
        for d in 'd', 'def', 'defaults':
            self.assertEqual(git.gitz(d), DEFAULTS)

    @repo.test
    def test_error(self):
        with self.assertRaises(ValueError):
            git.gitz('var')

        with self.assertRaises(ValueError):
            git.gitz('Com')


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
