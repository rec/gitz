from . import repo
from gitz.program import PROGRAM
import unittest


class GitLsTest(unittest.TestCase):
    @repo.test
    def test_change(self):
        repo.make_commit('1')
        repo.make_commit('2')
        actual = PROGRAM.git.ls()
        expected = [
            '0   \t.* ago\tc0d1dbb 0',
            '1   \t.* ago\ta03c0f8 1',
            '2   \t.* ago\t043df1f 2',
        ]
        for a, e in zip(actual, expected):
            self.assertRegex(a, e)
        self.assertEqual(len(actual), len(expected))
