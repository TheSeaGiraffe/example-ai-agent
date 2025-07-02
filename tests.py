import unittest
from pathlib import Path

from functions.get_file_content import MAX_CONTENT_LENGTH, get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file


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

    def get_golden_file(self, golden_file: str) -> str:
        with open(golden_file) as golden:
            return golden.read()

    def test_lorem(self):
        got = get_file_content(self.working_dir, "lorem-test.txt")
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


class TestWriteFile(unittest.TestCase):
    lorem_file_path = "calculator/lorem.txt"

    def read_file(self) -> str:
        with open(self.lorem_file_path) as lorem:
            return lorem.read()

    def write_file(self, contents: str):
        with open(self.lorem_file_path, "w") as lorem:
            lorem.write(contents)

    def test_lorem(self):
        old_lorem = self.read_file()
        got = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        want = 'Successfully wrote to "lorem.txt" (28 characters written)'
        self.write_file(old_lorem)
        self.assertEqual(got, want)

    def test_pkg_more_lorem(self):
        got = write_file(
            "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
        )
        want = 'Successfully wrote to "pkg/morelorem.txt" (26 characters written)'
        Path("calculator/pkg/morelorem.txt").unlink(missing_ok=True)
        self.assertEqual(got, want)

    def test_tmp_text(self):
        got = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        want = 'Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory'
        self.assertEqual(got, want)


class TestRunFile(unittest.TestCase):
    def test_run_calc_main(self):
        got = run_python_file("calculator", "main.py")
        want = 'STDOUT: Calculator App\nUsage: python main.py "<expression>"\nExample: python main.py "3 + 5"\n'

        self.assertEqual(got, want)

    def test_run_calc_tests(self):
        got = run_python_file("calculator", "tests.py")

        want_parts = ["STDERR", "Ran 9 tests", "OK"]
        for want_part in want_parts:
            self.assertIn(want_part, got)

    # Should error
    def test_run_agent_main(self):
        got = run_python_file("calculator", "../main.py")
        want = 'Error: Cannot execute "../main.py" as it is outside the permitted working directory'

        self.assertEqual(got, want)

    # Should error
    def test_run_nonexistent(self):
        got = run_python_file("calculator", "nonexistent.py")
        want = 'Error: File "nonexistent.py" not found.'

        self.assertEqual(got, want)


if __name__ == "__main__":
    unittest.main()
