from . import repo
from gitz.program import git
import os
import unittest


class GitInferTest(unittest.TestCase):
    @repo.test
    def test_change(self):
        with self.assertRaises(Exception):
            git.infer()

        with open('0', 'w') as fp:
            fp.write('1\n')

        with self.assertRaises(Exception):
            git.infer()
        actual = git.infer('-a')
        expected = [
            '[master 9fbfd4a] Update 0',
            ' 1 file changed, 1 insertion(+), 1 deletion(-)',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_add(self):
        with open('1', 'w') as fp:
            fp.write('1\n')
        git.add('1')
        actual = git.infer()
        expected = [
            '[master 0ae685e] Add 1',
            ' 1 file changed, 1 insertion(+)',
            ' create mode 100644 1',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_remove(self):
        repo.make_commit('1')
        os.remove('0')
        actual = git.infer('-a')
        expected = [
            '[master 3897048] Delete 0',
            ' 1 file changed, 1 deletion(-)',
            ' delete mode 100644 0',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_rename(self):
        git.mv('0', '1')
        actual = git.infer()
        expected = [
            '[master e147e06] Rename 0 -> 1',
            ' 1 file changed, 0 insertions(+), 0 deletions(-)',
            ' rename 0 => 1 (100%)',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_multiple(self):
        repo.make_commit('1')
        repo.make_commit('2')
        git.mv('0', '3')
        os.remove('1')

        with open('4', 'w') as fp:
            fp.write('4\n')

        with open('2', 'w') as fp:
            fp.write('6\n')
        git.add('2', '4')

        actual = git.infer()
        expected = [
            '[master 624f20c] Several changes',
            ' 3 files changed, 2 insertions(+), 1 deletion(-)',
            ' rename 0 => 3 (100%)',
            ' create mode 100644 4',
        ]
        self.assertEqual(actual, expected)
