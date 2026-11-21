"""小さな実装課題の作業フォルダを作る。使い方: gen_code_ws.py <出力先> <ラベル（未使用）>"""
import pathlib, sys
ws = pathlib.Path(sys.argv[1]); ws.mkdir(parents=True, exist_ok=True)
(ws / "README.md").write_text("# textkit\n\nImplement `slugify` and `wrap_title` in `textkit.py` so that `python3 -m unittest -q` passes. Do not edit the tests.\n")
(ws / "textkit.py").write_text('"""Text helpers."""\n\n\ndef slugify(text: str, max_len: int = 40) -> str:\n    raise NotImplementedError\n\n\ndef wrap_title(text: str, width: int) -> list[str]:\n    raise NotImplementedError\n')
(ws / "test_textkit.py").write_text('''import unittest
from textkit import slugify, wrap_title


class SlugTests(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_collapse_and_trim(self):
        self.assertEqual(slugify("  --A  b__c--  "), "a-b-c")

    def test_unicode_folded(self):
        self.assertEqual(slugify("Crème Brûlée à la carte"), "creme-brulee-a-la-carte")

    def test_max_len_cuts_at_word_boundary(self):
        self.assertEqual(slugify("alpha beta gamma delta", max_len=12), "alpha-beta")

    def test_single_long_word_is_hard_cut(self):
        self.assertEqual(slugify("abcdefghijklmnop", max_len=8), "abcdefgh")

    def test_empty_falls_back(self):
        self.assertEqual(slugify("!!!"), "untitled")


class WrapTests(unittest.TestCase):
    def test_wrap(self):
        self.assertEqual(wrap_title("the quick brown fox jumps", 10), ["the quick", "brown fox", "jumps"])

    def test_long_word_kept_whole(self):
        self.assertEqual(wrap_title("a extraordinarily b", 5), ["a", "extraordinarily", "b"])

    def test_bad_width(self):
        with self.assertRaises(ValueError):
            wrap_title("x", 0)


if __name__ == "__main__":
    unittest.main()
''')
