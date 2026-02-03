import unittest

from gitz.git import GIT, functions, repo


class GitCopyTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        GIT.new('one')
        GIT.copy('two', '-v')
        expected = {'origin': ['main', 'one', 'two'], 'upstream': ['main']}
        self.assertEqual(functions.remote_branches(), expected)
