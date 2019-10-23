from . import repo
from gitz.runner import GIT
import os
import unittest


class GitInferTest(unittest.TestCase):
    @repo.test
    def test_change(self):
        with self.assertRaises(Exception):
            GIT.infer()

        with open('0', 'w') as fp:
            fp.write('1\n')

        with self.assertRaises(Exception):
            GIT.infer()
        actual = GIT.infer('-a')
        expected = [
            '[master 7f6a5c7] Modified 0',
            ' 1 file changed, 1 insertion(+), 1 deletion(-)',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_add(self):
        with open('1', 'w') as fp:
            fp.write('1\n')
        GIT.add('1')
        actual = GIT.infer()
        expected = [
            '[master f2ebcf8] Added 1',
            ' 1 file changed, 1 insertion(+)',
            ' create mode 100644 1',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_remove(self):
        repo.make_commit('1')
        os.remove('0')
        actual = GIT.infer('-a')
        expected = [
            '[master df2ea01] Deleted 0',
            ' 1 file changed, 1 deletion(-)',
            ' delete mode 100644 0',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_rename(self):
        GIT.mv('0', '1')
        actual = GIT.infer()
        expected = [
            '[master 3e8619b] Renamed 0 -> 1',
            ' 1 file changed, 0 insertions(+), 0 deletions(-)',
            ' rename 0 => 1 (100%)',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_multiple(self):
        repo.make_commit('1')
        repo.make_commit('2')
        GIT.mv('0', '3')
        os.remove('1')

        with open('4', 'w') as fp:
            fp.write('4\n')

        with open('2', 'w') as fp:
            fp.write('6\n')
        GIT.add('2', '4')

        actual = GIT.infer()
        expected = [
            '[master 91234c6] Several changes',
            ' 3 files changed, 2 insertions(+), 1 deletion(-)',
            ' rename 0 => 3 (100%)',
            ' create mode 100644 4',
        ]
        self.assertEqual(actual, expected)
