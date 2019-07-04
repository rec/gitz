import unittest
from . import repo


class RepoTest(unittest.TestCase):
    @repo.method
    def test_repo(self):
        self.assertEqual('8c0a320', repo.make_commit('one.txt'))
        with self.assertRaises(Exception):
            repo.make_commit('one.txt')

        self.assertEqual('d150342', repo.make_commit('two.txt'))
