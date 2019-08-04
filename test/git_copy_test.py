from . import repo
from gitz import git_functions
from gitz.program import PROGRAM
import unittest


class GitCopyTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        PROGRAM.git.fresh('one')
        PROGRAM.git.copy('two')
        expected = {'origin': ['master', 'one', 'two'], 'upstream': ['master']}
        self.assertEqual(git_functions.all_branches(), expected)
