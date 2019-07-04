import unittest
from . import repo_maker


class RepoTest(unittest.TestCase):
    def test_repo(self):
        with repo_maker.git_repo():
            c1 = repo_maker.make_commit('one.txt')
            with self.assertRaises(Exception):
                repo_maker.make_commit('one.txt')
            c2 = repo_maker.make_commit('two.txt')
            self.assertEqual(c1, '8c0a320')
            self.assertEqual(c2, 'd150342')
