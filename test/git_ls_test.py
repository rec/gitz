from . import repo
import unittest
GIT = repo.GIT


class GitLsTest(unittest.TestCase):
    @repo.method
    def test_change(self):
        repo.make_commit('0')
        repo.make_commit('1')
        repo.make_commit('2')
        actual = GIT.ls()
        expected = [
            '0   \t.* ago\td748b2f 0',
            '1   \t.* ago\t9db4688 1',
            '2   \t.* ago\t90c348e 2',
        ]
        for a, e in zip(actual, expected):
            self.assertRegex(a, e)
        self.assertEqual(len(actual), len(expected))
