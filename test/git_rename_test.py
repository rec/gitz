from . import repo
from gitz import git
from gitz.git import GIT
import unittest


class GitRenameTest(unittest.TestCase):
    @repo.method
    def test_simple(self):
        repo.make_commit('1')
        GIT.fresh('one')
        GIT.rename('two')
        expected = {'origin': ['master', 'two'], 'upstream': ['master']}
        self.assertEqual(git.all_branches(), expected)
