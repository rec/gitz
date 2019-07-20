from . import repo
from gitz import git_functions
from gitz.git import GIT
import unittest


class GitRotateTest(unittest.TestCase):
    @repo.method
    def test_change(self):
        GIT.checkout('-b', 'A')
        repo.make_commit('1')

        GIT.checkout('-b', 'B')
        repo.make_commit('2')

        GIT.checkout('-b', 'C')
        repo.make_commit('3')
        self.assertEqual(git_functions.current_branch(), 'C')

        GIT.rotate('0')
        self.assertEqual(git_functions.current_branch(), 'C')

        GIT.rotate()
        self.assertEqual(git_functions.current_branch(), 'master')

        GIT.rotate()
        self.assertEqual(git_functions.current_branch(), 'A')

        GIT.rotate('2')
        self.assertEqual(git_functions.current_branch(), 'C')

        GIT.rotate('-1')
        self.assertEqual(git_functions.current_branch(), 'B')

        GIT.rotate('-')
        self.assertEqual(git_functions.current_branch(), 'A')

        GIT.rotate('-2')
        self.assertEqual(git_functions.current_branch(), 'C')
