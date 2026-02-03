import unittest

from gitz.git import GIT, repo


class GitAdjustTest(unittest.TestCase):
    @repo.test
    def test_default(self):
        repo.make_seven_commits(self)
        GIT.reset('--soft', 'HEAD~')
        GIT.adjust('-v')
        actual = GIT.log('--oneline')[:4]
        expected = ['84e8ee1 6', '8a4a4e2 5', 'a7c7e8f 4', '9ab30c5 3']
        self.assertEqual(expected, actual)

        self.assertEqual(['6', '7'], _files_in_commit())

    @repo.test
    def test_simple(self):
        repo.make_seven_commits(self)
        GIT.reset('--soft', 'HEAD~')
        GIT.adjust('HEAD~', '-v')
        actual = GIT.log('--oneline')[:4]
        expected = ['0e103e7 6', '207bd13 5', 'a7c7e8f 4', '9ab30c5 3']
        self.assertEqual(expected, actual)

        self.assertEqual(['6'], _files_in_commit())
        self.assertEqual(['5', '7'], _files_in_commit('HEAD~'))

    @repo.test
    def test_commit(self):
        repo.make_seven_commits(self)
        GIT.adjust('HEAD~3', '--commit=HEAD~', '-v')
        actual = GIT.log('--oneline')[:4]
        expected = ['18f631a 7', '6c901a6 5', '9375333 4', '9ab30c5 3']
        self.assertEqual(expected, actual)

        self.assertEqual(['7'], _files_in_commit())
        self.assertEqual(['5'], _files_in_commit('HEAD~'))
        self.assertEqual(['4', '6'], _files_in_commit('HEAD~~'))

    @repo.test
    def test_message(self):
        repo.make_seven_commits(self)
        GIT.adjust('HEAD~3', '--commit=HEAD~', '-m', '4 and 6', '-v')
        actual = GIT.log('--oneline')[:4]
        expected = ['d43e4a8 7', 'e38207c 5', 'ac920db 4 and 6', '9ab30c5 3']
        self.assertEqual(expected, actual)

        self.assertEqual(['7'], _files_in_commit())
        self.assertEqual(['5'], _files_in_commit('HEAD~'))
        self.assertEqual(['4', '6'], _files_in_commit('HEAD~~'))

    @repo.test
    def test_all_tracked(self):
        repo.make_seven_commits(self)
        repo.write_file('6', 'DELTA')
        GIT.adjust('-a', '-v')
        actual = GIT.log('--oneline')[:4]
        expected = ['067af20 7', 'e1e931a 6', '8a4a4e2 5', 'a7c7e8f 4']
        self.assertEqual(expected, actual)

        self.assertEqual(['6', '7'], _files_in_commit())

    @repo.test
    def test_all_files(self):
        repo.make_seven_commits(self)
        GIT.reset('HEAD~')
        GIT.adjust('-A', '-v')
        actual = GIT.log('--oneline')[:4]
        expected = ['84e8ee1 6', '8a4a4e2 5', 'a7c7e8f 4', '9ab30c5 3']
        self.assertEqual(expected, actual)

        self.assertEqual(['6', '7'], _files_in_commit())


def _files_in_commit(commit='HEAD'):
    return GIT.diff_tree('--no-commit-id', '--name-only', '-r', commit)
