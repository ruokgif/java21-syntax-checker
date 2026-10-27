import os
import sys
import unittest
import tkinter as tk

sys.path.insert(0, os.path.abspath("."))
from gui.app import JavaSyntaxCheckerApp


class TestBracketAndQuotePairing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.app = JavaSyntaxCheckerApp(cls.root)
        cls.editor = cls.app.editor

    @classmethod
    def tearDownClass(cls):
        try:
            cls.root.destroy()
        except Exception:
            pass

    def setUp(self):
        self.editor.clear()
        self.editor.text.delete("1.0", "end")
        self.editor.text.edit_reset()

    def _type_char(self, char):
        event = tk.Event()
        event.char = char
        event.keysym = char
        event.state = 0
        res = self.editor._on_key_press(event)
        if res != "break":
            self.editor.text.insert("insert", char)
        self.editor._on_key_release(event)
        self.root.update()

    def _press_backspace(self):
        event = tk.Event()
        event.char = "\x08"
        event.keysym = "BackSpace"
        event.state = 0
        res = self.editor._on_backspace(event)
        if res != "break":
            if self.editor.text.compare("insert", ">", "1.0"):
                self.editor.text.delete("insert-1c")
        self.editor._on_key_release(event)
        self.root.update()

    def _press_return(self):
        event = tk.Event()
        event.char = "\r"
        event.keysym = "Return"
        event.state = 0
        res = self.editor._on_return(event)
        if res != "break":
            self.editor.text.insert("insert", "\n")
        self.editor._on_key_release(event)
        self.root.update()

    # 1. Typing ( inserts () with the cursor between them.
    def test_01_paren_pairing(self):
        self._type_char("(")
        self.assertEqual(self.editor.get_content(), "()")
        self.assertEqual(self.editor.text.index("insert"), "1.1")

    # 2. Typing { inserts {} with the cursor between them.
    def test_02_brace_pairing(self):
        self._type_char("{")
        self.assertEqual(self.editor.get_content(), "{}")
        self.assertEqual(self.editor.text.index("insert"), "1.1")

    # 3. Typing [ inserts [] with the cursor between them.
    def test_03_bracket_pairing(self):
        self._type_char("[")
        self.assertEqual(self.editor.get_content(), "[]")
        self.assertEqual(self.editor.text.index("insert"), "1.1")

    # 4. Typing " inserts paired double quotes.
    def test_04_double_quote_pairing(self):
        self._type_char('"')
        self.assertEqual(self.editor.get_content(), '""')
        self.assertEqual(self.editor.text.index("insert"), "1.1")

    # 5. Typing ' inserts paired single quotes.
    def test_05_single_quote_pairing(self):
        self._type_char("'")
        self.assertEqual(self.editor.get_content(), "''")
        self.assertEqual(self.editor.text.index("insert"), "1.1")

    # 6. Typing a closing character skips over an existing matching closer.
    def test_06_skip_closing_characters(self):
        for open_ch, close_ch in [("(", ")"), ("[", "]"), ("{", "}"), ('"', '"'), ("'", "'")]:
            self.editor.clear()
            self._type_char(open_ch)
            self.assertEqual(self.editor.get_content(), open_ch + close_ch)
            self.assertEqual(self.editor.text.index("insert"), "1.1")
            # Type the closing character
            self._type_char(close_ch)
            # Should skip over without duplicating
            self.assertEqual(self.editor.get_content(), open_ch + close_ch)
            self.assertEqual(self.editor.text.index("insert"), "1.2")

    # 7. Backspace between an empty pair removes both characters.
    def test_07_backspace_pair_deletion(self):
        for open_ch, close_ch in [("(", ")"), ("[", "]"), ("{", "}"), ('"', '"'), ("'", "'")]:
            self.editor.clear()
            self._type_char(open_ch)
            self.assertEqual(self.editor.get_content(), open_ch + close_ch)
            self.assertEqual(self.editor.text.index("insert"), "1.1")
            # Press Backspace
            self._press_backspace()
            self.assertEqual(self.editor.get_content(), "")
            self.assertEqual(self.editor.text.index("insert"), "1.0")

    # 8. Enter between {} creates a properly indented multiline block.
    def test_08_enter_between_braces(self):
        self.editor.set_content("class Test ")
        self.editor.text.mark_set("insert", "1.11")
        self._type_char("{")
        self.assertEqual(self.editor.get_content(), "class Test {}")
        self.assertEqual(self.editor.text.index("insert"), "1.12")
        self._press_return()
        expected = "class Test {\n    \n}"
        self.assertEqual(self.editor.get_content(), expected)
        self.assertEqual(self.editor.text.index("insert"), "2.4")

    # Nested Enter between {}
    def test_08b_nested_enter_between_braces(self):
        self.editor.set_content("    void foo() ")
        self.editor.text.mark_set("insert", "1.15")
        self._type_char("{")
        self.assertEqual(self.editor.get_content(), "    void foo() {}")
        self.assertEqual(self.editor.text.index("insert"), "1.16")
        self._press_return()
        expected = "    void foo() {\n        \n    }"
        self.assertEqual(self.editor.get_content(), expected)
        self.assertEqual(self.editor.text.index("insert"), "2.8")

    # 9. Existing syntax highlighting continues to work.
    def test_09_syntax_highlighting_preservation(self):
        code = "public class Demo {\n    int count = 100;\n}"
        self.editor.set_content(code)
        self.editor._apply_syntax_highlight()
        # Verify syntax keywords/types are tagged
        kw_tags = self.editor.text.tag_ranges("syntax_kw")
        self.assertTrue(len(kw_tags) > 0, "syntax_kw should be tagged for public/class")
        type_tags = self.editor.text.tag_ranges("syntax_type")
        self.assertTrue(len(type_tags) > 0, "syntax_type should be tagged for int")

    # 10. Line numbers remain synchronized after inserting and deleting pairs.
    def test_10_line_numbers_synchronization(self):
        self.editor.set_content("class Test ")
        self.editor.text.mark_set("insert", "1.11")
        self._type_char("{")
        self._press_return()
        # Verify 3 lines in editor and gutter
        lines = self.editor.line_canvas.get("1.0", "end-1c").strip().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[-1].strip(), "3")
        # Backspace newline
        self.editor.text.mark_set("insert", "2.4")
        self._press_backspace()
        self.root.update()
        lines_after = self.editor.line_canvas.get("1.0", "end-1c").strip().splitlines()
        self.assertTrue(len(lines_after) <= 3)

    # 11. Undo and redo work correctly.
    def test_11_undo_and_redo(self):
        self._type_char("(")
        self.assertEqual(self.editor.get_content(), "()")
        self.editor.text.edit_undo()
        self.assertEqual(self.editor.get_content(), "")
        self.editor.text.edit_redo()
        self.assertEqual(self.editor.get_content(), "()")

    # Selection wrapping
    def test_13_selection_wrapping(self):
        self.editor.set_content("x + y")
        self.editor.text.tag_add("sel", "1.0", "1.5")
        self.editor.text.mark_set("insert", "1.5")
        self._type_char("(")
        self.assertEqual(self.editor.get_content(), "(x + y)")

        # Wrap with quotes
        self.editor.set_content("greeting")
        self.editor.text.tag_add("sel", "1.0", "1.8")
        self.editor.text.mark_set("insert", "1.8")
        self._type_char('"')
        self.assertEqual(self.editor.get_content(), '"greeting"')

    # Quote closing inside string does not double-close
    def test_14_quote_inside_string_does_not_double(self):
        self.editor.set_content('String msg = "hello')
        self.editor.text.mark_set("insert", "1.19")
        self._type_char('"')
        self.assertEqual(self.editor.get_content(), 'String msg = "hello"')


if __name__ == "__main__":
    unittest.main()
