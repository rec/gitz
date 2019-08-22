from . import repo
from gitz.program import git
import unittest


class GitAmpTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        git.checkout('-b', 'develop')

        git.push('--set-upstream', 'origin', 'develop')
        git.amp('Hello', 'there', 'mates')
        actual = git.log('--oneline')
        expected = ['1974b10 Hello there mates', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        actual = git.log('--oneline', 'origin/develop')
        self.assertEqual(actual, expected)
