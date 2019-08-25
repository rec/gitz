from . import repo
from gitz.program import git
from gitz.program import safe_git
import unittest


class GitFreshTest(unittest.TestCase):
    @repo.test
    def test_fresh(self):
        git.fresh('one')
        repo.make_commit('1')
        git.push()
        actual = safe_git.log('--oneline', 'origin/one')
        expected = ['a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        git.fresh('two')
        repo.make_commit('2')
        git.push()
        actual = safe_git.log('--oneline', 'origin/two')
        expected = ['aff4d90 2', 'c0d1dbb 0']
        self.assertEqual(actual, expected)
