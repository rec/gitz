from . import repo
from gitz.git import GIT
import unittest


class GitFreshTest(unittest.TestCase):
    @repo.test
    def test_fresh(self):
        GIT.fresh('one')
        repo.make_commit('1')
        GIT.push()
        actual = GIT.log('--oneline', 'origin/one')
        expected = ['a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        GIT.fresh('two')
        repo.make_commit('2')
        GIT.push()
        actual = GIT.log('--oneline', 'origin/two')
        expected = ['aff4d90 2', 'c0d1dbb 0']
        self.assertEqual(actual, expected)
