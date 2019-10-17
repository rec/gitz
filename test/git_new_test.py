from . import repo
from gitz.runner import GIT
from gitz.runner import GIT_INFO
import unittest


class GitNewTest(unittest.TestCase):
    @repo.test
    def test_new(self):
        GIT.new('one')
        repo.make_commit('1')
        GIT.push()
        actual = GIT_INFO.log('--oneline', 'origin/one')
        expected = ['a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        GIT.new('two')
        repo.make_commit('2')
        GIT.push()
        actual = GIT_INFO.log('--oneline', 'origin/two')
        expected = ['aff4d90 2', 'c0d1dbb 0']
        self.assertEqual(actual, expected)
