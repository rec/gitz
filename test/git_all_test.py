from . import repo
from pathlib import Path
import unittest

GIT = repo.GIT


class GitAllTest(unittest.TestCase):
    def test_directories(self):
        actual = GIT.all('test/data/*', '-', 'ls', '-1')
        self.assertEqual(actual, _DIRECTORIES.split('\n'))

    @repo.method
    def test_branches(self):
        self.assertEqual('047f436', repo.make_commit('one.txt'))
        current = GIT.current_branch()
        GIT.checkout('-b', 'foo')
        self.assertEqual(repo.make_commit('two.txt'), '33bb2c0')
        GIT.checkout(current)
        GIT.checkout('-b', 'bar')
        self.assertEqual(repo.make_commit('three.txt'), '79715f1')
        actual = GIT.all('-', 'git', 'log', '--oneline')
        print(*actual, sep='\n')
        self.assertEqual(actual, _BRANCHES.split('\n'))


_DIRECTORIES = """\
Directory {0}/data/bar:
  one.txt
  two.txt

Directory {0}/data/foo:
  three.txt
""".format(
    str(Path(__file__).parent)
)

_BRANCHES = """\
Branch bar:
  79715f1 three.txt
  047f436 one.txt

Branch foo:
  33bb2c0 two.txt
  047f436 one.txt

Branch master:
  047f436 one.txt
"""
