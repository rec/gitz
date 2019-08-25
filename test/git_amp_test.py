from . import repo
from gitz.program import safe_git
import unittest


class GitAmpTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        safe_git.checkout('-b', 'develop')

        safe_git.push('--set-upstream', 'origin', 'develop')
        safe_git.amp('Hello', 'there', 'mates')
        actual = safe_git.log('--oneline')
        expected = ['1974b10 Hello there mates', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        actual = safe_git.log('--oneline', 'origin/develop')
        self.assertEqual(actual, expected)
