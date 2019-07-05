import unittest
from . import repo


class RepoTest(unittest.TestCase):
    @repo.method
    def test_repo(self):
        self.assertEqual('047f436', repo.make_commit('one.txt'))
        with self.assertRaises(Exception):
            repo.make_commit('one.txt')

        self.assertEqual('33bb2c0', repo.make_commit('two.txt'))
