from . import repo
from gitz.program import safe_git
import unittest


class GitLsTest(unittest.TestCase):
    @repo.test
    def test_change(self):
        repo.make_commit('1')
        repo.make_commit('2')
        actual = safe_git.when()
        expected = [
            r'0.* ago.*c0d1dbb.*0.*',
            r'1.* ago.*a03c0f8.*1.*',
            r'2.* ago.*043df1f.*2.*',
        ]
        for a, e in zip(actual, expected):
            self.assertRegex(a, e)
        self.assertEqual(len(actual), len(expected))
