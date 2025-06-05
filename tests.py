import unittest

from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def test_calculator_root(self):
        got = get_files_info("calculator", ".")
        self.assertIn("main.py", got)
        self.assertIn("pkg", got)
        self.assertIn("tests.py", got)

    def test_calculator_pkg(self):
        got = get_files_info("calculator", "pkg")
        self.assertIn("calculator.py", got)
        self.assertIn("render.py", got)

    def test_calculator_bin(self):
        got = get_files_info("calculator", "/bin")
        self.assertEqual('Error: "/bin" is not a directory', got)

    def test_calculator_parent(self):
        got = get_files_info("calculator", "../")
        self.assertEqual(
            'Error: Cannot list "../" as it is outside the permitted working directory',
            got,
        )


if __name__ == "__main__":
    unittest.main()
