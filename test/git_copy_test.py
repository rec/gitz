from . import repo
from gitz import git_functions
from gitz.program import dry_git
import unittest


class GitCopyTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        dry_git.fresh('one')
        dry_git.copy('two')
        expected = {'origin': ['master', 'one', 'two'], 'upstream': ['master']}
        self.assertEqual(git_functions.all_branches(), expected)
