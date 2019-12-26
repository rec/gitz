from . import repo
from gitz.git import GIT
import unittest


class GitNewTest(unittest.TestCase):
    @repo.test
    def test_new(self):
        GIT.new('one', '-v')
        repo.make_commit('1')
        GIT.push()
        actual = GIT.log('--oneline', 'origin/one')
        expected = ['a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        GIT.new('two', '-v')
        repo.make_commit('2')
        GIT.push()
        actual = GIT.log('--oneline', 'origin/two')
        expected = ['aff4d90 2', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

    @repo.test
    def test_use_head(self):
        GIT.new('one', '-vu')
        repo.make_commit('1')
        GIT.push()
        actual = GIT.log('--oneline', 'origin/one')
        expected = ['a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        GIT.new('two', '-vu')
        repo.make_commit('2')
        GIT.push()
        actual = GIT.log('--oneline', 'origin/two')
        expected = ['043df1f 2', 'a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

    @repo.test
    def test_use_head_unstaged(self):
        repo.make_commit('1')
        repo.write_file('1', '2')
        GIT.new('one', '-vu')
        with open('1') as fp:
            self.assertEqual(fp.read(), '2')
        actual = GIT.log('--oneline', 'origin/one')
        expected = ['a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)
