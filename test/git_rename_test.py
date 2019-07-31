from . import repo
from gitz import git_functions
from gitz.git import GIT
import unittest


class GitRenameTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        GIT.fresh('one')
        GIT.rename('two')
        expected = {'origin': ['master', 'two'], 'upstream': ['master']}
        self.assertEqual(git_functions.all_branches(), expected)
