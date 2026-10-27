import os
import sys
import unittest
import tkinter as tk

# Ensure gui module is importable
sys.path.insert(0, os.path.abspath("."))
from gui.app import ParserBackend, JavaSyntaxCheckerApp, LineNumberText

class TestGUIIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.backend = ParserBackend()
        cls.root = tk.Tk()
        cls.root.withdraw()  # Hide window during automated test
        cls.app = JavaSyntaxCheckerApp(cls.root)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.root.destroy()
        except Exception:
            pass

    def test_window_title_and_structure(self):
        """Verify window title, subcomponents, and default state."""
        self.assertIn("Java Syntax Checker", self.app.root.title())
        self.assertIsNotNone(self.app.editor)
        self.assertIsNotNone(self.app.command_palette)
        self.assertIsNotNone(self.app.result_label)

    def test_backend_initialization(self):
        """Verify backend loads javacheck.dll via ctypes or initializes fallback."""
        if self.backend.use_dll:
            self.assertIsNotNone(self.backend.dll, "ctypes CDLL handle should not be None when use_dll is True")
        else:
            self.assertIsNone(self.backend.dll)

    def test_valid_simple_class(self):
        """Test checking a valid simple Java class string."""
        code = "public class Simple { int x = 10; }"
        ret, msg, err_line = self.backend.check_code_string(code)
        self.assertEqual(ret, 0)
        self.assertIn("SUCCESS", msg)
        self.assertIsNone(err_line)

    def test_valid_java21_features(self):
        """Test checking a valid Java 21 record and switch pattern program."""
        code = """
        public class Java21Demo {
            record Point(double x, double y) {}
            String eval(Object o) {
                return switch (o) {
                    case null -> "null";
                    case Point(double x, double y) when x > 0 -> "positive point";
                    default -> "other";
                };
            }
        }
        """
        ret, msg, err_line = self.backend.check_code_string(code)
        self.assertEqual(ret, 0)
        self.assertIn("SUCCESS", msg)
        self.assertIsNone(err_line)

    def test_invalid_line_1(self):
        """Test invalid Java with error on line 1."""
        code = "class {\n}"
        ret, msg, err_line = self.backend.check_code_string(code)
        self.assertEqual(ret, 1)
        self.assertEqual(err_line, 1)
        self.assertIn("Line 1", msg)

    def test_invalid_middle_line(self):
        """Test invalid Java with error on line 4."""
        code = "class Test {\n    int a = 10;\n    void run() {\n        int y = ;\n    }\n}"
        ret, msg, err_line = self.backend.check_code_string(code)
        self.assertEqual(ret, 1)
        self.assertEqual(err_line, 4)
        self.assertIn("Line 4", msg)

    def test_invalid_after_comments_and_blank_lines(self):
        """Test invalid Java with error on line 6 after comments and blank lines."""
        code = "// Comment 1\n// Comment 2\n\nclass Test {\n\n    int bad = ;\n}"
        ret, msg, err_line = self.backend.check_code_string(code)
        self.assertEqual(ret, 1)
        self.assertEqual(err_line, 6)

    def test_invalid_eof(self):
        """Test invalid Java with missing closing brace at EOF."""
        code = "class Test {\n    void run() {\n        System.out.println();\n}"
        ret, msg, err_line = self.backend.check_code_string(code)
        self.assertEqual(ret, 1)
        self.assertIn("ERROR", msg)

    def test_gui_file_load_and_line_numbers(self):
        """Test loading an external .java file into the GUI editor and verifying line numbers."""
        test_file = os.path.abspath("tests/valid_1.java")
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.app.path_var.set(test_file)
        self.app.editor.set_content(content)

        self.assertEqual(self.app.editor.get_content(), content)
        # Check line number canvas content
        line_count = int(self.app.editor.text.index("end-1c").split(".")[0])
        canvas_text = self.app.editor.line_canvas.get("1.0", "end-1c").strip()
        last_line_num = int(canvas_text.splitlines()[-1].strip())
        self.assertEqual(last_line_num, line_count)

    def test_gui_editor_editing_and_rechecking(self):
        """Test user workflow: load invalid code -> check -> see error -> fix -> check -> see success."""
        # 1. Invalid code
        invalid_code = "class Demo {\n    int x = ;\n}"
        self.app.editor.set_content(invalid_code)
        self.app.on_check_syntax()

        self.assertIn("Syntax Error detected at line 2", self.app.result_label.cget("text"))
        tags = self.app.editor.text.tag_ranges("error_line")
        self.assertTrue(len(tags) > 0)
        self.assertEqual(self.app.editor.text.index(tags[0]), "2.0")

        # 2. Fix code in editor
        fixed_code = "class Demo {\n    int x = 42;\n}"
        self.app.editor.set_content(fixed_code)
        self.app.on_check_syntax()

        self.assertIn("Parsing Successful: No syntax errors detected.", self.app.result_label.cget("text"))
        tags = self.app.editor.text.tag_ranges("error_line")
        self.assertEqual(len(tags), 0, "Error tag should be cleared upon success")

    def test_gui_error_highlight_and_clearing(self):
        """Test GUI editor widget text setting, error highlighting, and clearing."""
        code = "class Test {\n    int x = ;\n}"
        self.app.editor.set_content(code)
        self.assertEqual(self.app.editor.get_content(), code)

        self.app.on_check_syntax()
        self.assertIn("Syntax Error detected at line 2", self.app.result_label.cget("text"))

        # Verify error highlight tag is added on line 2
        tags = self.app.editor.text.tag_ranges("error_line")
        self.assertTrue(len(tags) > 0, "Error line tag should be active")
        self.assertEqual(self.app.editor.text.index(tags[0]), "2.0")

        # Test on_clear
        self.app.on_clear()
        self.assertEqual(self.app.editor.get_content(), "")
        self.assertEqual(len(self.app.editor.text.tag_ranges("error_line")), 0)
        self.assertEqual(self.app.path_var.get(), "")

    def test_gui_long_file_scrolling_and_line_numbers(self):
        """Test loading a large multi-line source file and verifying scroll & line number sync."""
        lines = ["// Line " + str(i) for i in range(1, 101)]
        lines.append("class LongTest { int val = 100; }")
        long_code = "\n".join(lines)

        self.app.editor.set_content(long_code)
        self.assertEqual(self.app.editor.get_content(), long_code)

        canvas_text = self.app.editor.line_canvas.get("1.0", "end-1c").strip().splitlines()
        self.assertEqual(len(canvas_text), 101)
        self.assertEqual(canvas_text[-1].strip(), "101")

        # Check syntax of long file
        self.app.on_check_syntax()
        self.assertIn("Parsing Successful: No syntax errors detected.", self.app.result_label.cget("text"))

    def test_empty_source_handling(self):
        """Test checking empty source code."""
        ret, msg, err_line = self.backend.check_code_string("   \n\t  ")
        self.assertEqual(ret, 2)
        self.assertIn("empty", msg.lower())

    def test_command_palette_toggle_and_filtering(self):
        """Test Command Palette visibility toggling, searching, and filtering."""
        # Open palette
        self.app.toggle_command_palette()
        self.assertTrue(self.app.command_palette.is_visible)

        # Test filter search
        self.app.command_palette._filter_commands("Syntax")
        self.assertTrue(len(self.app.command_palette.filtered_items) >= 1)
        self.assertEqual(self.app.command_palette.filtered_items[0][0], "Check Syntax")

        # Close palette via escape/hide
        self.app.command_palette.hide()
        self.assertFalse(self.app.command_palette.is_visible)

if __name__ == "__main__":
    unittest.main(verbosity=2)
