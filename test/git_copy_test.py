from gitz.git import GIT
from gitz.git import functions
from gitz.git import repo
import unittest


class GitCopyTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        GIT.new('one')
        GIT.copy('two', '-v')
        expected = {'origin': ['master', 'one', 'two'], 'upstream': ['master']}
        self.assertEqual(functions.remote_branches(), expected)
