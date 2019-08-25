from . import repo
from gitz.program import git
from gitz.program import safe_git
import unittest


def psp():
    print(*safe_git.status('--porcelain'), sep='\n')


class GitSplitTest(unittest.TestCase):
    @repo.test
    def test_multiple(self):
        repo.make_commit('1', '2')
        repo.make_commit('3', '4')
        repo.make_commit('5')
        git.mv('0', '6')
        git.commit('-am', '6')
        with self.assertRaises(Exception):
            git.split('HEAD~~~~')
        git.split('HEAD~~~')
        actual = safe_git.log('--oneline')
        expected = [
            '78923d2 [split] Renamed 0 -> 6',
            'ed73fa3 [split] Added 5',
            '2605324 [split] Added 4',
            '96e0ea3 [split] Added 3',
            '3c32b33 [split] Added 2',
            '5bb18ae [split] Added 1',
            'c0d1dbb 0',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_single(self):
        repo.make_commit('1', '2')
        repo.make_commit('3', '4', '5')
        git.split()
        actual = safe_git.log('--oneline', '-10')
        expected = [
            'a804db6 [split] Added 5',
            '125a73b [split] Added 4',
            'f92b5f4 [split] Added 3',
            '57c4c87 1_2',
            'c0d1dbb 0',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_staging_area(self):
        repo.make_commit('1')
        repo.make_commit('2')
        repo.write_files('3', '4')
        repo.add_files('3')
        git.mv('1', '5')
        git.rm('0')
        git.split()
        actual = safe_git.log('--oneline', '-10')
        expected = [
            'cea714a [split] Added 4',
            '05ecff4 [split] Renamed 1 -> 5',
            'e6b7f89 [split] Added 3',
            '21f80f5 [split] Deleted 0',
            '043df1f 2',
            'a03c0f8 1',
            'c0d1dbb 0',
        ]
        self.assertEqual(actual, expected)
