from . import repo
from gitz.git import functions
from gitz.program import GIT
import unittest


class GitRotateTest(unittest.TestCase):
    @repo.test
    def test_change(self):
        GIT.checkout('-b', 'A')
        repo.make_commit('1')

        GIT.checkout('-b', 'B')
        repo.make_commit('2')

        GIT.checkout('-b', 'C')
        repo.make_commit('3')
        self.assertEqual(functions.branch_name(), 'C')

        GIT.rotate('0')
        self.assertEqual(functions.branch_name(), 'C')

        GIT.rotate()
        self.assertEqual(functions.branch_name(), 'master')

        GIT.rotate()
        self.assertEqual(functions.branch_name(), 'A')

        GIT.rotate('2')
        self.assertEqual(functions.branch_name(), 'C')

        GIT.rotate('-1')
        self.assertEqual(functions.branch_name(), 'B')

        GIT.rotate('-')
        self.assertEqual(functions.branch_name(), 'A')

        GIT.rotate('-2')
        self.assertEqual(functions.branch_name(), 'C')
