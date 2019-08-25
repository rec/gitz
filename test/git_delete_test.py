from . import repo
from gitz import git_functions
from gitz.program import git
import unittest


class GitDeleteTest(unittest.TestCase):
    @repo.test
    def test_delete(self):
        git.fresh('one')
        repo.make_commit('1')
        git.push()

        git.fresh('two')
        repo.make_commit('2')
        git.push()

        actual = git_functions.branches('-r')
        expected = [
            'origin/master',
            'origin/one',
            'origin/two',
            'upstream/master',
        ]
        self.assertEqual(actual, expected)

        git.delete('one', 'two')
        actual = git_functions.branches('-r')
        expected = ['origin/master', 'upstream/master']
        self.assertEqual(actual, expected)
