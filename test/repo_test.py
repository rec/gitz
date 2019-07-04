import unittest
from . import repo_maker


class RepoTest(unittest.TestCase):
    @repo_maker.repo_method
    def test_repo(self):
        self.assertEqual('8c0a320', repo_maker.make_commit('one.txt'))
        with self.assertRaises(Exception):
            repo_maker.make_commit('one.txt')

        self.assertEqual('d150342', repo_maker.make_commit('two.txt'))
