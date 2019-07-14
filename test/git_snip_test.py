from . import repo
from gitz.git import GIT
import os
import unittest


class GitSnipTest(unittest.TestCase):
    @repo.method
    def test_simple(self):
        one = repo.make_commit('1')
        repo.make_commit('2')
        three = repo.make_commit('3')
        repo.make_commit('4')
        repo.make_commit('5')
        repo.make_commit('6')

        GIT.snip(one, three, 'HEAD~')
        files = [i for i in os.listdir() if not i.startswith('.')]
        self.assertEqual(sorted(files), ['0', '2', '4', '6'])
