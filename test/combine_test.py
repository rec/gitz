from gitz.git import combine
import unittest


class ShuffleTest(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(combine.shuffle('a'), [])
        self.assertEqual(combine.shuffle('ab'), [])
        self.assertEqual(combine.shuffle('abc'), [])

        self.assertEqual(combine.shuffle('a', True), [0, 1])
        self.assertEqual(combine.shuffle('ab', True), [0, 1, 2])
        self.assertEqual(combine.shuffle('abc', True), [0, 1, 2, 3])

    def test_swap(self):
        self.assertEqual(combine.shuffle('ba'), [1, 0, 2])

    def test_cycle(self):
        self.assertEqual(combine.shuffle('cab'), [2, 0, 1, 3])
        self.assertEqual(combine.shuffle('cabe'), [2, 0, 1, 4])
        self.assertEqual(combine.shuffle('dbcf'), [3, 1, 2, 5])
        self.assertEqual(combine.shuffle('ebcg'), [4, 1, 2, 6])
        self.assertEqual(combine.shuffle('hfgj'), [7, 5, 6, 9])

    def test_cleaning(self):
        self.assertEqual(combine.shuffle('cabdef'), [2, 0, 1, 3])
        self.assertEqual(combine.shuffle('cabedf'), [2, 0, 1, 4, 3, 5])
        self.assertEqual(combine.shuffle('abcdfe'), [0, 1, 2, 3, 5, 4, 6])
