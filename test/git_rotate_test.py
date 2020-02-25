from gitz.git import repo
from gitz.git import functions
from gitz.git import GIT
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

        GIT.rotate('0', '-v')
        self.assertEqual(functions.branch_name(), 'C')

        GIT.rotate('-v')
        self.assertEqual(functions.branch_name(), 'master')

        GIT.rotate('-v')
        self.assertEqual(functions.branch_name(), 'A')

        GIT.rotate('2', '-v')
        self.assertEqual(functions.branch_name(), 'C')

        GIT.rotate('-1', '-v')
        self.assertEqual(functions.branch_name(), 'B')

        GIT.rotate('-', '-v')
        self.assertEqual(functions.branch_name(), 'A')

        GIT.rotate('-2', '-v')
        self.assertEqual(functions.branch_name(), 'C')
