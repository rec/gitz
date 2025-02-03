from gitz.git import GIT
from gitz.git import functions
from gitz.git import repo
import unittest


class GitRotTest(unittest.TestCase):
    @repo.test
    def test_change(self):
        GIT.checkout('-b', 'A')
        repo.make_commit('1')

        GIT.checkout('-b', 'B')
        repo.make_commit('2')

        GIT.checkout('-b', 'C')
        repo.make_commit('3')
        self.assertEqual(functions.branch_name(), 'C')

        GIT.rot('0', '-v')
        self.assertEqual(functions.branch_name(), 'C')

        GIT.rot('-v')
        self.assertEqual(functions.branch_name(), 'main')

        GIT.rot('-v')
        self.assertEqual(functions.branch_name(), 'A')

        GIT.rot('2', '-v')
        self.assertEqual(functions.branch_name(), 'C')

        GIT.rot('-1', '-v')
        self.assertEqual(functions.branch_name(), 'B')

        GIT.rot('-', '-v')
        self.assertEqual(functions.branch_name(), 'A')

        GIT.rot('-2', '-v')
        self.assertEqual(functions.branch_name(), 'C')
