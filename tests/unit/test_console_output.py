from io import BytesIO, TextIOWrapper
import unittest
from unittest import mock

from scripts import setup_project


class ConsoleOutputTest(unittest.TestCase):
    def test_windows_console_escapes_diff_characters_outside_its_encoding(self) -> None:
        buffer = BytesIO()
        stream = TextIOWrapper(buffer, encoding="cp1252")

        with mock.patch.object(setup_project.sys, "stdout", stream):
            setup_project.configure_console_output()
            print("→")
            stream.flush()

        self.assertTrue(buffer.getvalue().startswith(b"\\u2192"))


if __name__ == "__main__":
    unittest.main()
