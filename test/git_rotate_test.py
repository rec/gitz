from . import repo
from gitz import git_functions
from gitz.program import PROGRAM
import unittest


class GitRotateTest(unittest.TestCase):
    @repo.test
    def test_change(self):
        PROGRAM.git.checkout('-b', 'A')
        repo.make_commit('1')

        PROGRAM.git.checkout('-b', 'B')
        repo.make_commit('2')

        PROGRAM.git.checkout('-b', 'C')
        repo.make_commit('3')
        self.assertEqual(git_functions.branch_name(), 'C')

        PROGRAM.git.rotate('0')
        self.assertEqual(git_functions.branch_name(), 'C')

        PROGRAM.git.rotate()
        self.assertEqual(git_functions.branch_name(), 'master')

        PROGRAM.git.rotate()
        self.assertEqual(git_functions.branch_name(), 'A')

        PROGRAM.git.rotate('2')
        self.assertEqual(git_functions.branch_name(), 'C')

        PROGRAM.git.rotate('-1')
        self.assertEqual(git_functions.branch_name(), 'B')

        PROGRAM.git.rotate('-')
        self.assertEqual(git_functions.branch_name(), 'A')

        PROGRAM.git.rotate('-2')
        self.assertEqual(git_functions.branch_name(), 'C')
