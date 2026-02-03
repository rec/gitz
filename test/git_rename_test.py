import unittest

from gitz.git import GIT, functions, repo


class GitRenameTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        GIT.new('one')
        GIT.rename('two', '-v')
        expected = {'origin': ['main', 'two'], 'upstream': ['main']}
        self.assertEqual(functions.remote_branches(), expected)
