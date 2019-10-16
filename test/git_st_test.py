from . import repo
from gitz.program import git
from gitz.program import git_info
import os
import unittest


class GitStTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1', '2')
        with open('3', 'w') as fp:
            fp.write('3\n')
        git.add('3')
        with open('4', 'w') as fp:
            fp.write('4\n')
        with open('0', 'w') as fp:
            fp.write('100\n')
        os.remove('1')

        actual = git_info.st()
        expected = [
            '\x1b[32mmaster\x1b[m',
            ' \x1b[31mM\x1b[m 0  | 2 \x1b[32m+\x1b[m\x1b[31m-\x1b[m',
            ' \x1b[31mD\x1b[m 1  | 1 \x1b[31m-\x1b[m',
            '\x1b[32mA\x1b[m  3  | 1 \x1b[32m+\x1b[m',
            '\x1b[31m??\x1b[m 4  ',
        ]
        self.assertEqual(actual, expected)
