from . import repo
from gitz.program import PROGRAM
import unittest


class GitAmpTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        PROGRAM.git_info.checkout('-b', 'develop')

        PROGRAM.git_info.push('--set-upstream', 'origin', 'develop')
        PROGRAM.git_info.amp('Hello', 'there', 'mates')
        actual = PROGRAM.git_info.log('--oneline')
        expected = ['1974b10 Hello there mates', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        actual = PROGRAM.git_info.log('--oneline', 'origin/develop')
        self.assertEqual(actual, expected)
