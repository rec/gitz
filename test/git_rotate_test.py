from . import repo
import unittest
GIT = repo.GIT


class GitRotateTest(unittest.TestCase):
    @repo.method
    def test_change(self):
        repo.make_commit('0')

        GIT.checkout('-b', 'A')
        repo.make_commit('1')

        GIT.checkout('-b', 'B')
        repo.make_commit('2')

        GIT.checkout('-b', 'C')
        repo.make_commit('3')
        self.assertEqual(GIT.current_branch(), 'C')

        GIT.rotate('0')
        self.assertEqual(GIT.current_branch(), 'C')

        GIT.rotate()
        self.assertEqual(GIT.current_branch(), 'master')

        GIT.rotate()
        self.assertEqual(GIT.current_branch(), 'A')

        GIT.rotate('2')
        self.assertEqual(GIT.current_branch(), 'C')

        GIT.rotate('-1')
        self.assertEqual(GIT.current_branch(), 'B')

        GIT.rotate('-')
        self.assertEqual(GIT.current_branch(), 'A')

        GIT.rotate('-2')
        self.assertEqual(GIT.current_branch(), 'C')
