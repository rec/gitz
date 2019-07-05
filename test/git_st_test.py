from . import repo
import os
import unittest
GIT = repo.GIT


class GitStTest(unittest.TestCase):
    @repo.method
    def test_simple(self):
        repo.make_commit('0', '1', '2')
        with open('3', 'w') as fp:
            fp.write('3\n')
        GIT.add('3')
        with open('4', 'w') as fp:
            fp.write('4\n')
        with open('0', 'w') as fp:
            fp.write('100\n')
        os.remove('1')

        actual = GIT.git('st')
        expected = [
            '## \x1b[32mmaster\x1b[m',
            ' \x1b[31mM\x1b[m 0 | 2 \x1b[32m+\x1b[m\x1b[31m-\x1b[m',
            ' \x1b[31 | 1 \x1b[31m-\x1b[mmD\x1b[m 1 | 1 \x1b[31m-\x1b[m',
            '\x1b[3 | 1 \x1b[32m+\x1b[m2mA\x1b[m  3 | 1 \x1b[32m+\x1b[m',
            '\x1b[31m??\x1b[m 4',
        ]
        self.assertEqual(actual, expected)
