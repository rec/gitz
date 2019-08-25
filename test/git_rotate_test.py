from . import repo
from gitz import git_functions
from gitz.program import dry_git
import unittest


class GitRotateTest(unittest.TestCase):
    @repo.test
    def test_change(self):
        dry_git.checkout('-b', 'A')
        repo.make_commit('1')

        dry_git.checkout('-b', 'B')
        repo.make_commit('2')

        dry_git.checkout('-b', 'C')
        repo.make_commit('3')
        self.assertEqual(git_functions.branch_name(), 'C')

        dry_git.rotate('0')
        self.assertEqual(git_functions.branch_name(), 'C')

        dry_git.rotate()
        self.assertEqual(git_functions.branch_name(), 'master')

        dry_git.rotate()
        self.assertEqual(git_functions.branch_name(), 'A')

        dry_git.rotate('2')
        self.assertEqual(git_functions.branch_name(), 'C')

        dry_git.rotate('-1')
        self.assertEqual(git_functions.branch_name(), 'B')

        dry_git.rotate('-')
        self.assertEqual(git_functions.branch_name(), 'A')

        dry_git.rotate('-2')
        self.assertEqual(git_functions.branch_name(), 'C')
