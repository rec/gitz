from gitz.git import GIT
from gitz.git import functions
from gitz.git import repo
import unittest


class GitRenameTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        GIT.new('one')
        GIT.rename('two', '-v')
        expected = {'origin': ['master', 'two'], 'upstream': ['master']}
        self.assertEqual(functions.remote_branches(), expected)
