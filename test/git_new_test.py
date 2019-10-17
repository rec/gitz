from . import repo
from gitz.program import PROGRAM
from gitz.runner import GIT_INFO
import unittest


class GitNewTest(unittest.TestCase):
    @repo.test
    def test_new(self):
        PROGRAM.git.new('one')
        repo.make_commit('1')
        PROGRAM.git.push()
        actual = GIT_INFO.log('--oneline', 'origin/one')
        expected = ['a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        PROGRAM.git.new('two')
        repo.make_commit('2')
        PROGRAM.git.push()
        actual = GIT_INFO.log('--oneline', 'origin/two')
        expected = ['aff4d90 2', 'c0d1dbb 0']
        self.assertEqual(actual, expected)
