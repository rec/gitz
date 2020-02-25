from gitz.git import repo
from gitz.git import functions
from gitz.git import GIT
import unittest


class GitSaveTest(unittest.TestCase):
    def _test(self):
        commit_id = repo.make_commit(changed='O')
        repo.write_files(changed='X', staged='staged', untracked='untracked')
        GIT.add('staged')
        expected = [' M changed', 'A  staged', '?? untracked']
        self.assertEqual(_status(), expected)
        return commit_id

    @repo.test
    def test_all(self):
        commit_id = self._test()
        status = _status()
        GIT.save('-a', '-v')
        self.assertEqual(commit_id, functions.commit_id())
        self.assertEqual(status, _status())
        GIT.reset('--hard', 'HEAD~')
        repo.make_seven_commits(self)
        GIT.save('pop', '-v')
        self.assertEqual(status, _status())

    @repo.test
    def test_regular(self):
        commit_id = self._test()
        status = _status()
        GIT.save('-v')
        self.assertEqual(commit_id, functions.commit_id())
        self.assertEqual(status, _status())
        GIT.reset('--hard', 'HEAD~')

        repo.make_seven_commits(self)
        GIT.save('pop', '-v')
        self.assertEqual(status[:-1], _status())


def _status():
    return GIT.status('--porcelain')
