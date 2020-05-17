from gitz.git import GIT
from gitz.git import repo
import unittest


def psp():
    print(*GIT.status('--porcelain'), sep='\n')


class GitSplitTest(unittest.TestCase):
    @repo.test
    def test_multiple(self):
        repo.make_commit('1', '2')
        repo.make_commit('3', '4')
        repo.make_commit('5')
        GIT.mv('0', '6')
        GIT.commit('-am', '6')
        with self.assertRaises(Exception):
            GIT.split('HEAD~~~~')
        GIT.split('HEAD~~~', '-v')
        actual = GIT.log('--oneline')
        expected = [
            '3a5be12 [split] Rename 0 -> 6',
            '32f71be [split] Add 5',
            '1268e55 [split] Add 4',
            'ecd3a2d [split] Add 3',
            'b2366e2 [split] Add 2',
            'd084861 [split] Add 1',
            'c0d1dbb 0',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_single(self):
        repo.make_commit('1', '2')
        repo.make_commit('3', '4', '5')
        GIT.split('-v')
        actual = GIT.log('--oneline', '-10')
        expected = [
            '30d81e9 [split] Add 5',
            '915d6ff [split] Add 4',
            '1144293 [split] Add 3',
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
        GIT.mv('1', '5')
        GIT.rm('0')
        GIT.split('-v')
        actual = GIT.log('--oneline', '-10')
        expected = [
            '8af7046 [split] Rename 1 -> 5',
            'df1744a [split] Add 3',
            'ad0dbfb [split] Delete 0',
            '043df1f 2',
            'a03c0f8 1',
            'c0d1dbb 0',
        ]
        self.assertEqual(actual, expected)
