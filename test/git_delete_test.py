from . import repo
from gitz import git_functions
from gitz.git import GIT
import unittest


class GitDeleteTest(unittest.TestCase):
    @repo.method
    def test_delete(self):
        GIT.fresh('one')
        repo.make_commit('1')
        GIT.push()

        GIT.fresh('two')
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

        GIT.delete('one', 'two')
        actual = git_functions.branches('-r')
        expected = ['origin/master', 'upstream/master']
        self.assertEqual(actual, expected)
