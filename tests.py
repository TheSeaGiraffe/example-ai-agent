import unittest
from pathlib import Path

from functions.get_file_content import MAX_CONTENT_LENGTH, get_file_content
from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    working_dir = "calculator"

    def test_calculator_root(self):
        got = get_files_info(self.working_dir, ".")
        self.assertIn("main.py", got)
        self.assertIn("pkg", got)
        self.assertIn("tests.py", got)

    def test_calculator_pkg(self):
        got = get_files_info(self.working_dir, "pkg")
        self.assertIn("calculator.py", got)
        self.assertIn("render.py", got)

    def test_calculator_bin(self):
        got = get_files_info(self.working_dir, "/bin")
        self.assertEqual('Error: "/bin" is not a directory', got)

    def test_calculator_parent(self):
        got = get_files_info(self.working_dir, "../")
        self.assertEqual(
            'Error: Cannot list "../" as it is outside the permitted working directory',
            got,
        )


class TestGetFileContent(unittest.TestCase):
    working_dir = "calculator"
    lorem_trunc_golden = "lorem_trunc.txt"
    golden_files = {
        "lorem": "lorem_trunc.txt",
        "calc_main": "calculator/main.py",
        "calc_calc": "calculator/pkg/calculator.py",
    }

    def get_golden_file(self, golden_file: Path) -> str:
        with open(golden_file) as golden:
            return golden.read()

    def test_lorem(self):
        got = get_file_content(self.working_dir, "lorem.txt")
        golden_file = self.golden_files["lorem"]
        lorem_trunc = f'{self.get_golden_file(golden_file)}...File "lorem.txt" truncated at {MAX_CONTENT_LENGTH} characters'
        self.assertEqual(lorem_trunc, got)

    def test_calc_main_file(self):
        got = get_file_content(self.working_dir, "main.py")
        golden_file = self.golden_files["calc_main"]
        want = self.get_golden_file(golden_file)
        self.assertEqual(got, want)

    def test_calculator_file(self):
        got = get_file_content(self.working_dir, "pkg/calculator.py")
        golden_file = self.golden_files["calc_calc"]
        want = self.get_golden_file(golden_file)
        self.assertEqual(got, want)

    def test_non_existant_cat_file(self):
        got = get_file_content(self.working_dir, "/bin/cat")
        want = 'Error: Cannot read "/bin/cat" as it is outside the permitted working directory'
        self.assertEqual(got, want)


if __name__ == "__main__":
    unittest.main()
