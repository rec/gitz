from . import repo
from gitz.git import GIT
from gitz.git import commit_range
import unittest


class CommitRangeTest(unittest.TestCase):
    @repo.test
    def test_trivial(self):
        self._test_both('HEAD', '0', 'e487041', 0)

    @repo.test
    def test_simple(self):
        self._test_one('HEAD', '', 'e487041', 1)

    @repo.test
    def test_simple2(self):
        self._test_one('HEAD~', 'HEAD', 'e487041', 2)

    @repo.test
    def test_multiple(self):
        self._test_both('e1e931a', '043df1f', 'e1e931a', 5)

    @repo.test
    def test_not_in_range(self):
        repo.make_seven_commits(self)
        GIT.reset('--hard', 'c0d1dbb')
        commit = repo.make_one_commit('foo', 'foo', 'foo')

        with self.assertRaises(ValueError) as cm:
            commit_range.commit_range(commit, '043df1f')
        expected = '043df1f, 56f456a not in the same history'
        self.assertEqual(cm.exception.args[0], expected)

    def _test_both(self, c1, c2, expected_child, expected_count):
        self._test_one(c1, c2, expected_child, expected_count)

        child, count = commit_range.commit_range(c2, c1)
        self.assertEqual(child, expected_child)
        self.assertEqual(count, expected_count)

    def _test_one(self, c1, c2, expected_child, expected_count):
        repo.make_seven_commits(self)
        child, count = commit_range.commit_range(c1, c2)
        self.assertEqual(child, expected_child)
        self.assertEqual(count, expected_count)
