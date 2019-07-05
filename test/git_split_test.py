from . import repo
import unittest
GIT = repo.GIT
GIT_SILENT = repo.GIT_SILENT

def psp():
    print(*GIT.status('--porcelain'), sep-'\n')


class GitSplitTest(unittest.TestCase):
    @repo.method
    def test_multiple(self):
        self.assertEqual(repo.make_commit('0'), 'd748b2f')
        repo.make_commit('1', '2')

        repo.make_commit('3', '4')
        repo.make_commit('5')
        GIT.mv('0', '6')
        GIT.commit('-am', '6')
        with self.assertRaises(Exception):
            GIT.split('HEAD~~~~')
        GIT.split('HEAD~~~')
        actual = GIT.log('--oneline')
        expected = [
            '2a0f88c [split] Renamed 0 -> 6',
            '41f3bb5 [split] Added 5',
            'd4c721f [split] Added 4',
            '9640105 [split] Added 3',
            '69b017d [split] Added 2',
            'e716475 [split] Added 1',
            'd748b2f 0',
        ]
        self.assertEqual(actual, expected)

    @repo.method
    def test_single(self):
        repo.make_commit('0', '1', '2')
        repo.make_commit('3', '4', '5')
        GIT.split()
        actual = GIT.log('--oneline', '-10')
        expected = [
            'a6da573 [split] Added 5',
            '7e35db0 [split] Added 4',
            'df9757a [split] Added 3',
            '4cb48bc 0_1_2',
        ]
        self.assertEqual(actual, expected)
