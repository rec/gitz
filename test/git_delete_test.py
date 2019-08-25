from . import repo
from gitz import git_functions
from gitz.program import dry_git
import unittest


class GitDeleteTest(unittest.TestCase):
    @repo.test
    def test_delete(self):
        dry_git.fresh('one')
        repo.make_commit('1')
        dry_git.push()

        dry_git.fresh('two')
        repo.make_commit('2')
        dry_git.push()

        actual = git_functions.branches('-r')
        expected = [
            'origin/master',
            'origin/one',
            'origin/two',
            'upstream/master',
        ]
        self.assertEqual(actual, expected)

        dry_git.delete('one', 'two')
        actual = git_functions.branches('-r')
        expected = ['origin/master', 'upstream/master']
        self.assertEqual(actual, expected)
