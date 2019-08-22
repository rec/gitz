from . import repo
from gitz import git_functions
from gitz.program import git
import unittest


class GitRotateTest(unittest.TestCase):
    @repo.test
    def test_change(self):
        git.checkout('-b', 'A')
        repo.make_commit('1')

        git.checkout('-b', 'B')
        repo.make_commit('2')

        git.checkout('-b', 'C')
        repo.make_commit('3')
        self.assertEqual(git_functions.branch_name(), 'C')

        git.rotate('0')
        self.assertEqual(git_functions.branch_name(), 'C')

        git.rotate()
        self.assertEqual(git_functions.branch_name(), 'master')

        git.rotate()
        self.assertEqual(git_functions.branch_name(), 'A')

        git.rotate('2')
        self.assertEqual(git_functions.branch_name(), 'C')

        git.rotate('-1')
        self.assertEqual(git_functions.branch_name(), 'B')

        git.rotate('-')
        self.assertEqual(git_functions.branch_name(), 'A')

        git.rotate('-2')
        self.assertEqual(git_functions.branch_name(), 'C')
