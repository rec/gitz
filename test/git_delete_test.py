from . import repo
from gitz import git_functions
from gitz.program import PROGRAM
import unittest


class GitDeleteTest(unittest.TestCase):
    @repo.test
    def test_delete(self):
        PROGRAM.git.fresh('one')
        repo.make_commit('1')
        PROGRAM.git.push()

        PROGRAM.git.fresh('two')
        repo.make_commit('2')
        PROGRAM.git.push()

        actual = git_functions.branches('-r')
        expected = [
            'origin/master',
            'origin/one',
            'origin/two',
            'upstream/master',
        ]
        self.assertEqual(actual, expected)

        PROGRAM.git.delete('one', 'two')
        actual = git_functions.branches('-r')
        expected = ['origin/master', 'upstream/master']
        self.assertEqual(actual, expected)
