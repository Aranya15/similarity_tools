import unittest

from similarity_tools import levenshtein, jaro_winkler


class TestLevenshtein(unittest.TestCase):
    def test_identical(self):
        self.assertEqual(levenshtein("kitten", "kitten"), 0)

    def test_empty_both(self):
        self.assertEqual(levenshtein("", ""), 0)

    def test_empty_one(self):
        self.assertEqual(levenshtein("", "abc"), 3)
        self.assertEqual(levenshtein("abc", ""), 3)

    def test_classic_example(self):
        self.assertEqual(levenshtein("kitten", "sitting"), 3)

    def test_substitution(self):
        self.assertEqual(levenshtein("flaw", "lawn"), 2)

    def test_insertion_deletion(self):
        self.assertEqual(levenshtein("abc", "ab"), 1)
        self.assertEqual(levenshtein("ab", "abc"), 1)

    def test_case_sensitive(self):
        self.assertEqual(levenshtein("a", "A"), 1)


class TestJaroWinkler(unittest.TestCase):
    def test_identical(self):
        self.assertAlmostEqual(jaro_winkler("hello", "hello"), 1.0)

    def test_empty_both(self):
        self.assertAlmostEqual(jaro_winkler("", ""), 1.0)

    def test_empty_one(self):
        self.assertAlmostEqual(jaro_winkler("", "abc"), 0.0)
        self.assertAlmostEqual(jaro_winkler("abc", ""), 0.0)

    def test_no_match(self):
        self.assertAlmostEqual(jaro_winkler("abc", "xyz"), 0.0)

    def test_known_value(self):
        # Standard example: MARTHA vs MARHTA
        self.assertAlmostEqual(jaro_winkler("MARTHA", "MARHTA"), 0.9611111111111111)

    def test_prefix_boost(self):
        # DIXON vs DICKSONX
        self.assertAlmostEqual(jaro_winkler("DIXON", "DICKSONX"), 0.8133333333333332)

    def test_case_sensitive(self):
        self.assertAlmostEqual(jaro_winkler("a", "A"), 0.0)

    def test_symmetric(self):
        a, b = "fuzzy", "fuzzing"
        self.assertAlmostEqual(jaro_winkler(a, b), jaro_winkler(b, a))

    def test_transposition(self):
        # "ab" vs "ba" should have no matches within window (max_dist=0)
        self.assertAlmostEqual(jaro_winkler("ab", "ba"), 0.0)


if __name__ == "__main__":
    unittest.main()
