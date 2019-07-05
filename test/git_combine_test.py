from . import repo
import os
import unittest

GIT = repo.GIT


class GitCombineTest(unittest.TestCase):
    @repo.method
    def test_simple(self):
        zero = repo.make_commit('0')
        repo.make_commit('1')
        repo.make_commit('2')
        three = repo.make_commit('3')
        repo.make_commit('4')
        repo.make_commit('5')
        repo.make_commit('6')

        GIT.git('combine', zero, three, 'HEAD~')
        files = [i for i in os.listdir() if not i.startswith('.')]
        self.assertEqual(files, ['0', '3', '5'])
