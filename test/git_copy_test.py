from . import repo
from gitz import git_functions
from gitz.runner import GIT
import unittest


class GitCopyTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        GIT.new('one')
        GIT.copy('two')
        expected = {'origin': ['master', 'one', 'two'], 'upstream': ['master']}
        self.assertEqual(git_functions.remote_branches(), expected)
