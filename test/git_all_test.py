from . import repo
from gitz import git_functions
from gitz.git import GIT
from gitz.program import PROGRAM
from pathlib import Path
import unittest


class GitAllTest(unittest.TestCase):
    def test_directories(self):
        # This needs to run in shell mode so that the * is expanded.
        # Either we need to run this in shell mode, or use glob.
        actual = GIT.all('test/data/*', '-', 'ls', '-1')
        self.assertEqual(actual, _DIRECTORIES.split('\n'))

    @repo.test
    def test_branches(self):
        self.assertEqual('44dac6b', repo.make_commit('one.txt'))
        current = git_functions.branch_name()
        PROGRAM.git.checkout('-b', 'foo')
        self.assertEqual(repo.make_commit('two.txt'), '393ad1c')
        PROGRAM.git.checkout(current)
        PROGRAM.git.checkout('-b', 'bar')
        self.assertEqual(repo.make_commit('three.txt'), 'b6aee43')
        actual = PROGRAM.git.all('-', 'git', 'log', '--oneline')
        print(*actual, sep='\n')
        self.assertEqual(actual, _BRANCHES.split('\n'))


_DIRECTORIES = """\
Directory {0}/data/bar:
  one.txt
  two.txt

Directory {0}/data/foo:
  three.txt
""".format(
    str(Path(__file__).parent)
)

_BRANCHES = """\
Branch bar:
  b6aee43 three.txt
  44dac6b one.txt
  c0d1dbb 0

Branch foo:
  393ad1c two.txt
  44dac6b one.txt
  c0d1dbb 0

Branch master:
  44dac6b one.txt
  c0d1dbb 0
"""
