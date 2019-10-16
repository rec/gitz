from . import repo
from gitz.program import git_info
import unittest


class GitAmpTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        git_info.checkout('-b', 'develop')

        git_info.push('--set-upstream', 'origin', 'develop')
        git_info.amp('Hello', 'there', 'mates')
        actual = git_info.log('--oneline')
        expected = ['1974b10 Hello there mates', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        actual = git_info.log('--oneline', 'origin/develop')
        self.assertEqual(actual, expected)
