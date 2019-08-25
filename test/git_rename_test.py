from . import repo
from gitz import git_functions
from gitz.program import dry_git
import unittest


class GitRenameTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        dry_git.fresh('one')
        dry_git.rename('two')
        expected = {'origin': ['master', 'two'], 'upstream': ['master']}
        self.assertEqual(git_functions.all_branches(), expected)
