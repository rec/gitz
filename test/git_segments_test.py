import unittest

from gitz.git.commit_segments import segments_to_commits


class GitSegmentsTest(unittest.TestCase):
    def test_simple(self):
        actual = list(segments_to_commits(''))
        expected = []
        self.assertEqual(actual, expected)

        actual = list(segments_to_commits('a'))
        expected = [('a', 0)]
        self.assertEqual(actual, expected)

        actual = list(segments_to_commits('ab'))
        expected = [('a', 0), ('b', 0)]
        self.assertEqual(actual, expected)

        actual = list(segments_to_commits('a+b'))
        expected = [('ab', 1)]
        self.assertEqual(actual, expected)

        actual = list(segments_to_commits('a-b'))
        expected = [('ab', 0)]
        self.assertEqual(actual, expected)

    def test_complex(self):
        actual = list(segments_to_commits('abc+de-fgh+i+j-k'))
        expected = [('a', 0), ('b', 0), ('cd', 1), ('ef', 0), ('g', 0), ('hijk', 2)]
        self.assertEqual(actual, expected)
