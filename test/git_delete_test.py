from . import repo
from gitz import git_functions
from gitz.runner import GIT
import unittest


class GitDeleteTest(unittest.TestCase):
    @repo.test
    def test_delete(self):
        GIT.new('one')
        repo.make_commit('1')
        GIT.push()

        GIT.new('two')
        repo.make_commit('2')
        GIT.push()

        actual = git_functions.branches('-r')
        expected = [
            'origin/master',
            'origin/one',
            'origin/two',
            'upstream/master',
        ]
        self.assertEqual(actual, expected)

        GIT.delete('-v', 'one', 'two')
        actual = git_functions.branches('-r')
        expected = ['origin/master', 'upstream/master']
        self.assertEqual(actual, expected)
