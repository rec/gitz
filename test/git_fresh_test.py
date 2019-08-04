from . import repo
from gitz.program import PROGRAM
import unittest


class GitFreshTest(unittest.TestCase):
    @repo.test
    def test_fresh(self):
        PROGRAM.git.fresh('one')
        repo.make_commit('1')
        PROGRAM.git.push()
        actual = PROGRAM.git.log('--oneline', 'origin/one')
        expected = ['a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        PROGRAM.git.fresh('two')
        repo.make_commit('2')
        PROGRAM.git.push()
        actual = PROGRAM.git.log('--oneline', 'origin/two')
        expected = ['aff4d90 2', 'c0d1dbb 0']
        self.assertEqual(actual, expected)
