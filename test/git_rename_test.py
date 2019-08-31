from . import repo
from gitz import git_functions
from gitz.program import git
import unittest


class GitRenameTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        git.fresh('one')
        git.rename('two')
        expected = {'origin': ['master', 'two'], 'upstream': ['master']}
        self.assertEqual(git_functions.remote_branches(), expected)
