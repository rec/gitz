from . import repo_maker
import unittest
import _gitz
GIT = _gitz.GIT


class GitAllTest(unittest.TestCase):
    def test_directories(self):
        actual = GIT.all('test/data/*', '-', 'ls', '-1')
        self.assertEqual(actual, _DIRECTORIES.split('\n'))

    @repo_maker.repo_method
    def test_branches(self):
        self.assertEqual('8c0a320', repo_maker.make_commit('one.txt'))
        current = GIT.current_branch()
        GIT.checkout('-b', 'foo')
        self.assertEqual(repo_maker.make_commit('two.txt'), 'd150342')
        GIT.checkout(current)
        GIT.checkout('-b', 'bar')
        self.assertEqual(repo_maker.make_commit('three.txt'), '79f4dec')
        actual = GIT.all('-', 'git', 'log', '--oneline')
        print(*actual, sep='\n')
        self.assertEqual(actual, _BRANCHES.split('\n'))



_DIRECTORIES = """\
Directory test/data/bar:
  one.txt
  two.txt

Directory test/data/foo:
  three.txt
"""

_BRANCHES = """\
Branch bar:
  79f4dec three.txt
  8c0a320 one.txt

Branch foo:
  d150342 two.txt
  8c0a320 one.txt

Branch master:
  8c0a320 one.txt
"""
