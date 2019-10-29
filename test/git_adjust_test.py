from . import repo
from gitz.git import GIT
import unittest


class GitAdjustTest(unittest.TestCase):
    @repo.test
    def test_default(self):
        repo.make_seven_commits(self)
        GIT.reset('--soft', 'HEAD~')
        GIT.adjust()
        actual = GIT.log('--oneline')[:4]
        expected = ['84e8ee1 6', '8a4a4e2 5', 'a7c7e8f 4', '9ab30c5 3']
        self.assertEqual(expected, actual)

        self.assertEqual(['6', '7'], _files_in_commit())

    @repo.test
    def test_simple(self):
        repo.make_seven_commits(self)
        GIT.reset('--soft', 'HEAD~')
        GIT.adjust('HEAD~')
        actual = GIT.log('--oneline')[:4]
        expected = ['0e103e7 6', '207bd13 5', 'a7c7e8f 4', '9ab30c5 3']
        self.assertEqual(expected, actual)

        self.assertEqual(['6'], _files_in_commit())
        self.assertEqual(['5', '7'], _files_in_commit('HEAD~'))

    @repo.test
    def test_edit(self):
        repo.make_seven_commits(self)
        GIT.adjust('HEAD~3', 'HEAD~')
        actual = GIT.log('--oneline')[:4]
        expected = ['18f631a 7', '6c901a6 5', '9375333 4', '9ab30c5 3']
        self.assertEqual(expected, actual)

        self.assertEqual(['7'], _files_in_commit())
        self.assertEqual(['5'], _files_in_commit('HEAD~'))
        self.assertEqual(['4', '6'], _files_in_commit('HEAD~~'))

    @repo.test
    def test_message(self):
        repo.make_seven_commits(self)
        GIT.adjust('HEAD~3', 'HEAD~', '-m', '4 and 6')
        actual = GIT.log('--oneline')[:4]
        expected = ['d43e4a8 7', 'e38207c 5', 'ac920db 4 and 6', '9ab30c5 3']
        self.assertEqual(expected, actual)

        self.assertEqual(['7'], _files_in_commit())
        self.assertEqual(['5'], _files_in_commit('HEAD~'))
        self.assertEqual(['4', '6'], _files_in_commit('HEAD~~'))


def _files_in_commit(commit='HEAD'):
    return GIT.diff_tree('--no-commit-id', '--name-only', '-r', commit)
