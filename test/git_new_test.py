from . import repo
from gitz.program import GIT
import unittest


class GitNewTest(unittest.TestCase):
    @repo.test
    def test_new(self):
        GIT.new('one')
        repo.make_commit('1')
        GIT.push()
        actual = GIT.log('--oneline', 'origin/one')
        expected = ['a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        GIT.new('two')
        repo.make_commit('2')
        GIT.push()
        actual = GIT.log('--oneline', 'origin/two')
        expected = ['aff4d90 2', 'c0d1dbb 0']
        self.assertEqual(actual, expected)
