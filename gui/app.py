"""
Java Syntax Checker — VS Code-Style Modern Command Palette GUI
Uses Flex Lexer + GNU Bison LALR(1) Parser via javacheck.dll / javacheck.exe.
"""

import os
import sys
import re
import tempfile
import ctypes
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# Resolve base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DLL_PATH = os.path.join(BASE_DIR, "javacheck.dll")
EXE_PATH = os.path.join(BASE_DIR, "javacheck.exe")

# Base64 Embedded 16x16 Application Icon (PNG)
APP_ICON_B64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGElEQVR42mNgqDrDQBEeNWDUgFEDhosBADHaRhCxp2aWAAAAAElFTkSuQmCC"

# Color Themes
THEMES = {
    "dark": {
        "bg_main": "#1e1e1e",
        "bg_panel": "#252526",
        "bg_output": "#181818",
        "bg_gutter": "#1e1e1e",
        "fg_main": "#d4d4d4",
        "fg_muted": "#858585",
        "fg_bright": "#ffffff",
        "fg_dim": "#6e6e6e",
        "border": "#282828",
        "accent": "#0e639c",
        "accent_hover": "#1177bb",
        "chip_bg": "#2d2d2d",
        "chip_hover": "#383838",
        "chip_fg": "#cccccc",
        "current_line": "#282828",
        "current_gutter_fg": "#ffffff",
        "error_line": "#5a1d1d",
        "error_line_fg": "#ffb3ba",
        "gutter_error_bg": "#5a1d1d",
        "gutter_error_fg": "#ff6b6b",
        "status_success_bg": "#16825d",
        "status_error_bg": "#a1260d",
        "status_neutral_bg": "#141414",
        "status_fg": "#ffffff",
        "output_success_fg": "#4ec9b0",
        "output_error_fg": "#f14c4c",
        "output_warn_fg": "#cca700",
        "output_cmd_fg": "#858585",
        "syntax_kw": "#569cd6",
        "syntax_type": "#4ec9b0",
        "syntax_str": "#ce9178",
        "syntax_comm": "#6a9955",
        "syntax_num": "#b5cea8",
        "syntax_anno": "#dcdcaa",
        "syntax_op": "#d4d4d4",
        "palette_bg": "#252526",
        "palette_border": "#007acc",
        "palette_input_bg": "#3c3c3c",
        "palette_sel_bg": "#04395e",
        "palette_sel_fg": "#ffffff",
        "scroll_trough": "#1e1e1e",
        "scroll_thumb": "#424242",
        "scroll_thumb_hover": "#5a5a5a",
        "scroll_thumb_drag": "#6e6e6e"
    },
    "light": {
        "bg_main": "#ffffff",
        "bg_panel": "#f3f3f3",
        "bg_output": "#f8f8f8",
        "bg_gutter": "#f3f3f3",
        "fg_main": "#1e1e1e",
        "fg_muted": "#717171",
        "fg_bright": "#000000",
        "fg_dim": "#888888",
        "border": "#e0e0e0",
        "accent": "#007acc",
        "accent_hover": "#005999",
        "chip_bg": "#e8e8e8",
        "chip_hover": "#dcdcdc",
        "chip_fg": "#333333",
        "current_line": "#f0f0f0",
        "current_gutter_fg": "#000000",
        "error_line": "#ffd2d2",
        "error_line_fg": "#900000",
        "gutter_error_bg": "#ffd2d2",
        "gutter_error_fg": "#b30000",
        "status_success_bg": "#107c41",
        "status_error_bg": "#d83b01",
        "status_neutral_bg": "#e8e8e8",
        "status_fg": "#1e1e1e",
        "output_success_fg": "#107c41",
        "output_error_fg": "#d83b01",
        "output_warn_fg": "#b28900",
        "output_cmd_fg": "#717171",
        "syntax_kw": "#0000ff",
        "syntax_type": "#267f99",
        "syntax_str": "#a31515",
        "syntax_comm": "#008000",
        "syntax_num": "#098658",
        "syntax_anno": "#795e26",
        "syntax_op": "#000000",
        "palette_bg": "#f3f3f3",
        "palette_border": "#007acc",
        "palette_input_bg": "#ffffff",
        "palette_sel_bg": "#cce8ff",
        "palette_sel_fg": "#000000",
        "scroll_trough": "#f3f3f3",
        "scroll_thumb": "#c1c1c1",
        "scroll_thumb_hover": "#a6a6a6",
        "scroll_thumb_drag": "#8c8c8c"
    }
}

JAVA_TYPES = {
    "boolean", "byte", "char", "double", "float", "int", "long", "short", "void", "var",
    "Boolean", "Byte", "Character", "Class", "Double", "Enum", "Float", "Integer", "Long",
    "Number", "Object", "Package", "Record", "Short", "String", "StringBuffer", "StringBuilder",
    "System", "Thread", "Throwable", "Exception", "RuntimeException", "Error", "Iterable",
    "Collection", "List", "ArrayList", "LinkedList", "Set", "HashSet", "TreeSet", "Map",
    "HashMap", "TreeMap", "Optional", "Arrays", "Collections", "Objects", "Math"
}

JAVA_KEYWORDS = {
    "abstract", "assert", "break", "case", "catch", "class", "const", "continue",
    "default", "do", "else", "enum", "exports", "extends", "final", "finally",
    "for", "goto", "if", "implements", "import", "instanceof", "interface",
    "module", "native", "new", "non-sealed", "open", "opens", "package",
    "permits", "private", "protected", "provides", "public", "record", "requires",
    "return", "sealed", "static", "strictfp", "super", "switch", "synchronized",
    "this", "throw", "throws", "to", "transient", "transitive", "try", "uses",
    "volatile", "when", "while", "with", "yield", "true", "false", "null"
}


class ParserBackend:
    """Interface to the Flex/Bison Java 21 parser (DLL / subprocess)."""

    def __init__(self):
        self.use_dll = False
        self.dll = None
        self._init_backend()

    def _init_backend(self):
        if os.path.exists(DLL_PATH):
            try:
                self.dll = ctypes.CDLL(DLL_PATH)
                self.dll.check_syntax.argtypes = [
                    ctypes.c_char_p,
                    ctypes.c_char_p,
                    ctypes.c_int
                ]
                self.dll.check_syntax.restype = ctypes.c_int
                self.use_dll = True
            except Exception:
                self.use_dll = False
                self.dll = None

    def check_file(self, filepath):
        """Check syntax of a .java file on disk. Returns (ret_code, message_str, error_line)."""
        abs_path = os.path.abspath(filepath)
        if not os.path.exists(abs_path):
            return 2, f"ERROR: File '{filepath}' does not exist.", None

        ret = 1
        msg = ""

        if self.use_dll and self.dll is not None:
            try:
                buf = ctypes.create_string_buffer(2048)
                ret = self.dll.check_syntax(abs_path.encode('utf-8'), buf, 2048)
                msg = buf.value.decode('utf-8', errors='replace')
            except Exception as e:
                return 2, f"ERROR: DLL execution failed: {str(e)}", None
        else:
            target_exe = EXE_PATH
            if not os.path.exists(target_exe):
                return 2, "ERROR: Neither javacheck.dll nor javacheck.exe is available.", None
            try:
                p = subprocess.run([target_exe, abs_path], capture_output=True, text=True, timeout=10)
                ret = p.returncode
                msg = (p.stdout + p.stderr).strip()
            except Exception as e:
                return 2, f"ERROR: Parser execution failed: {str(e)}", None

        error_line = None
        if ret != 0:
            match = re.search(r"Line\s+(\d+)", msg, re.IGNORECASE)
            if match:
                try:
                    error_line = int(match.group(1))
                except ValueError:
                    error_line = None

        return ret, msg, error_line

    def check_code_string(self, code_text):
        """Check syntax of code provided as an in-memory string."""
        if not code_text.strip():
            return 2, "ERROR: Source code editor is empty.", None

        temp_filename = ""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False, encoding='utf-8') as tf:
                tf.write(code_text)
                temp_filename = tf.name

            ret, msg, err_line = self.check_file(temp_filename)
        finally:
            if temp_filename and os.path.exists(temp_filename):
                try:
                    os.remove(temp_filename)
                except OSError:
                    pass

        return ret, msg, err_line


class ThinScrollbar(tk.Canvas):
    """Custom thin (10px) Canvas scrollbar following dark/light theme."""

    def __init__(self, parent, orient="vertical", command=None, theme=None, *args, **kwargs):
        self.orient = orient
        self.command = command
        self.theme = theme or THEMES["dark"]
        self.first = 0.0
        self.last = 1.0
        self._dragging = False
        self._drag_start_pos = 0
        self._drag_start_first = 0.0
        self._hover = False

        width = 10 if orient == "vertical" else None
        height = 10 if orient == "horizontal" else None

        super().__init__(
            parent,
            width=width,
            height=height,
            bg=self.theme["scroll_trough"],
            highlightthickness=0,
            border=0,
            *args, **kwargs
        )

        self.bind("<Configure>", self._redraw)
        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def set_theme(self, theme):
        self.theme = theme
        self.config(bg=theme["scroll_trough"])
        self._redraw()

    def set(self, first, last):
        try:
            self.first = max(0.0, min(1.0, float(first)))
            self.last = max(0.0, min(1.0, float(last)))
        except Exception:
            self.first = 0.0
            self.last = 1.0
        self._redraw()

    def _redraw(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()

        if self._dragging:
            thumb_color = self.theme["scroll_thumb_drag"]
        elif self._hover:
            thumb_color = self.theme["scroll_thumb_hover"]
        else:
            thumb_color = self.theme["scroll_thumb"]

        if self.orient == "vertical":
            if h <= 0 or (self.first == 0.0 and self.last == 1.0):
                return
            y1 = int(self.first * h)
            y2 = int(self.last * h)
            if y2 - y1 < 20:
                y2 = min(h, y1 + 20)
                if y2 == h and y1 > 0:
                    y1 = max(0, h - 20)
            self.create_rectangle(1, y1, w - 1, y2, fill=thumb_color, outline="", tags="thumb")
        else:
            if w <= 0 or (self.first == 0.0 and self.last == 1.0):
                return
            x1 = int(self.first * w)
            x2 = int(self.last * w)
            if x2 - x1 < 20:
                x2 = min(w, x1 + 20)
                if x2 == w and x1 > 0:
                    x1 = max(0, w - 20)
            self.create_rectangle(x1, 1, x2, h - 1, fill=thumb_color, outline="", tags="thumb")

    def _on_enter(self, event):
        self._hover = True
        self._redraw()

    def _on_leave(self, event):
        self._hover = False
        self._redraw()

    def _on_click(self, event):
        self._dragging = True
        if self.orient == "vertical":
            h = max(1, self.winfo_height())
            y1 = int(self.first * h)
            y2 = max(y1 + 20, int(self.last * h))
            if y1 <= event.y <= y2:
                self._drag_start_pos = event.y
                self._drag_start_first = self.first
            else:
                # Click on trough
                new_first = max(0.0, min(1.0 - (self.last - self.first), event.y / h))
                if self.command:
                    self.command("moveto", new_first)
                self._drag_start_pos = event.y
                self._drag_start_first = new_first
        else:
            w = max(1, self.winfo_width())
            x1 = int(self.first * w)
            x2 = max(x1 + 20, int(self.last * w))
            if x1 <= event.x <= x2:
                self._drag_start_pos = event.x
                self._drag_start_first = self.first
            else:
                new_first = max(0.0, min(1.0 - (self.last - self.first), event.x / w))
                if self.command:
                    self.command("moveto", new_first)
                self._drag_start_pos = event.x
                self._drag_start_first = new_first
        self._redraw()

    def _on_drag(self, event):
        if not self._dragging:
            return
        if self.orient == "vertical":
            h = max(1, self.winfo_height())
            delta = (event.y - self._drag_start_pos) / h
            span = max(0.01, self.last - self.first)
            new_first = max(0.0, min(1.0 - span, self._drag_start_first + delta))
            if self.command:
                self.command("moveto", new_first)
        else:
            w = max(1, self.winfo_width())
            delta = (event.x - self._drag_start_pos) / w
            span = max(0.01, self.last - self.first)
            new_first = max(0.0, min(1.0 - span, self._drag_start_first + delta))
            if self.command:
                self.command("moveto", new_first)

    def _on_release(self, event):
        self._dragging = False
        self._redraw()


class LineNumberText(tk.Frame):
    """VS Code-style code editor with synchronized line numbering, syntax coloring, and error highlights."""

    def __init__(self, parent, theme, on_cursor_move=None, on_edit=None, *args, **kwargs):
        super().__init__(parent, bg=theme["bg_main"], *args, **kwargs)

        self.theme = theme
        self.font_size = 11
        self.font = ("Consolas", self.font_size)
        self.on_cursor_move = on_cursor_move
        self.on_edit = on_edit
        self._highlight_job = None
        self.error_line_num = None
        self._ignore_edit_event = False

        # Custom Thin Scrollbars
        self.v_scrollbar = ThinScrollbar(self, orient="vertical", command=self._on_v_scroll, theme=theme)
        self.v_scrollbar.pack(side="right", fill="y")

        self.h_scrollbar = ThinScrollbar(self, orient="horizontal", command=self._on_h_scroll, theme=theme)
        self.h_scrollbar.pack(side="bottom", fill="x")

        # Gutter Container
        self.gutter_frame = tk.Frame(self, bg=theme["bg_gutter"], borderwidth=0)
        self.gutter_frame.pack(side="left", fill="y")

        self.line_canvas = tk.Text(
            self.gutter_frame,
            width=4,
            padx=0,
            pady=12,
            takefocus=0,
            border=0,
            relief="flat",
            highlightthickness=0,
            background=theme["bg_gutter"],
            foreground=theme["fg_muted"],
            state="disabled",
            font=self.font,
            wrap="none",
            spacing1=0,
            spacing2=0,
            spacing3=0,
            selectbackground=theme["bg_gutter"]
        )
        self.line_canvas.pack(side="left", fill="both", expand=True, padx=(8, 12))

        self.separator = tk.Frame(self, bg=theme["border"], width=1)
        self.separator.pack(side="left", fill="y")

        # Main Text Editor Area
        self.text = tk.Text(
            self,
            font=self.font,
            wrap="none",
            undo=True,
            padx=10,
            pady=12,
            border=0,
            relief="flat",
            spacing1=0,
            spacing2=0,
            spacing3=0,
            background=theme["bg_main"],
            foreground=theme["fg_main"],
            insertbackground=theme["fg_main"],
            insertwidth=2,
            selectbackground="#264f78" if theme == THEMES["dark"] else "#cce8ff",
            selectforeground="#ffffff" if theme == THEMES["dark"] else "#000000",
            highlightthickness=0
        )
        self.text.pack(side="left", fill="both", expand=True)

        self.text.config(
            xscrollcommand=self.h_scrollbar.set,
            yscrollcommand=self._on_text_yscroll
        )

        self._configure_tags()

        # Empty Editor State Overlay
        self.empty_overlay = tk.Frame(self.text, bg=theme["bg_main"])
        self.empty_title = tk.Label(
            self.empty_overlay,
            text="Java 21 Syntax Checker",
            font=("Segoe UI", 12, "bold"),
            fg=theme["fg_muted"],
            bg=theme["bg_main"]
        )
        self.empty_title.pack(pady=(0, 3))

        self.empty_sub = tk.Label(
            self.empty_overlay,
            text="Open a .java file or start typing",
            font=("Segoe UI", 9),
            fg=theme["fg_dim"],
            bg=theme["bg_main"]
        )
        self.empty_sub.pack(pady=(0, 5))

        self.empty_hint = tk.Label(
            self.empty_overlay,
            text="Ctrl+O · Ctrl+Enter",
            font=("Segoe UI", 8),
            fg=theme["fg_dim"],
            bg=theme["bg_main"]
        )
        self.empty_hint.pack()

        for w in (self.empty_overlay, self.empty_title, self.empty_sub, self.empty_hint):
            w.bind("<Button-1>", lambda e: self.text.focus_set())

        # Bindings
        self.text.bind("<Tab>", self._on_tab)
        self.text.bind("<Shift-Tab>", self._on_shift_tab)
        self.text.bind("<ISO_Left_Tab>", self._on_shift_tab)
        self.text.bind("<Return>", self._on_return)
        self.text.bind("<BackSpace>", self._on_backspace)
        self.text.bind("<KeyRelease>", self._on_key_release)
        self.text.bind("<KeyPress>", self._on_key_press)
        self.text.bind("<MouseWheel>", self._on_content_change)
        self.text.bind("<Button-1>", self._on_content_change)
        self.text.bind("<ButtonRelease-1>", self._on_content_change)

        # Gutter mouse wheel forwarding
        self.line_canvas.bind("<MouseWheel>", self._on_gutter_mousewheel)
        self.gutter_frame.bind("<MouseWheel>", self._on_gutter_mousewheel)
        self.line_canvas.bind("<Button-4>", lambda e: self.text.yview_scroll(-1, "units"))
        self.line_canvas.bind("<Button-5>", lambda e: self.text.yview_scroll(1, "units"))
        self.gutter_frame.bind("<Button-4>", lambda e: self.text.yview_scroll(-1, "units"))
        self.gutter_frame.bind("<Button-5>", lambda e: self.text.yview_scroll(1, "units"))

        self.update_line_numbers()
        self._check_empty_state()

    def _on_tab(self, event=None):
        """Indent current line or selected lines by exactly 4 spaces."""
        self.empty_overlay.place_forget()
        try:
            sel_start = self.text.index("sel.first")
            sel_end = self.text.index("sel.last")
        except tk.TclError:
            sel_start = None
            sel_end = None

        if sel_start and sel_end:
            start_line = int(sel_start.split(".")[0])
            end_line = int(sel_end.split(".")[0])
            if int(sel_end.split(".")[1]) == 0 and end_line > start_line:
                end_line -= 1
            for line in range(start_line, end_line + 1):
                self.text.insert(f"{line}.0", "    ")
            self.text.tag_add("sel", f"{start_line}.0", f"{end_line}.end")
        else:
            self.text.insert("insert", "    ")

        self._on_content_change()
        if self.on_edit and not self._ignore_edit_event:
            self.on_edit()
        self.schedule_syntax_highlight()
        return "break"

    def _on_shift_tab(self, event=None):
        """Outdent current line or selected lines by up to 4 spaces."""
        try:
            sel_start = self.text.index("sel.first")
            sel_end = self.text.index("sel.last")
        except tk.TclError:
            sel_start = None
            sel_end = None

        if sel_start and sel_end:
            start_line = int(sel_start.split(".")[0])
            end_line = int(sel_end.split(".")[0])
            if int(sel_end.split(".")[1]) == 0 and end_line > start_line:
                end_line -= 1
            for line in range(start_line, end_line + 1):
                line_text = self.text.get(f"{line}.0", f"{line}.end")
                spaces_to_remove = min(4, len(line_text) - len(line_text.lstrip(' ')))
                if spaces_to_remove > 0:
                    self.text.delete(f"{line}.0", f"{line}.{spaces_to_remove}")
            self.text.tag_add("sel", f"{start_line}.0", f"{end_line}.end")
        else:
            cur_line = int(self.text.index("insert").split(".")[0])
            line_text = self.text.get(f"{cur_line}.0", f"{cur_line}.end")
            spaces_to_remove = min(4, len(line_text) - len(line_text.lstrip(' ')))
            if spaces_to_remove > 0:
                self.text.delete(f"{cur_line}.0", f"{cur_line}.{spaces_to_remove}")

        self._on_content_change()
        if self.on_edit and not self._ignore_edit_event:
            self.on_edit()
        self.schedule_syntax_highlight()
        return "break"

    def _on_return(self, event=None):
        """Auto-indent next line to match current indentation, format multiline block between braces, or +4 spaces if line ended with '{'."""
        self.empty_overlay.place_forget()
        try:
            sel_start = self.text.index("sel.first")
            sel_end = self.text.index("sel.last")
            if sel_start and sel_end and self.text.compare(sel_start, "<", sel_end):
                self.text.delete("sel.first", "sel.last")
        except tk.TclError:
            pass

        cursor_idx = self.text.index("insert")
        line_num, col = map(int, cursor_idx.split("."))
        line_text = self.text.get(f"{line_num}.0", f"{line_num}.{col}")

        # Compute leading whitespace
        indent_len = len(line_text) - len(line_text.lstrip(' '))
        base_indent = " " * indent_len

        prev_char = self.text.get("insert-1c") if self.text.compare("insert", ">", "1.0") else ""
        next_char = self.text.get("insert")

        # Feature 5: Smart Enter between Braces
        rest_of_line = self.text.get("insert", f"{line_num}.end")
        if prev_char == "{" and (next_char == "}" or (rest_of_line.strip() == "}" and rest_of_line.endswith("}"))):
            if next_char != "}":
                close_brace_idx = self.text.search("}", "insert", f"{line_num}.end")
                if close_brace_idx:
                    self.text.delete("insert", close_brace_idx)
            indent_str = "    "
            self.text.edit_separator()
            self.text.insert("insert", "\n" + base_indent + indent_str + "\n" + base_indent)
            target = f"{line_num + 1}.{len(base_indent) + len(indent_str)}"
            self.text.mark_set("insert", target)
            self.text.edit_separator()
            self.text.see("insert")
            self._on_content_change()
            if self.on_edit and not self._ignore_edit_event:
                self.on_edit()
            self.schedule_syntax_highlight()
            return "break"

        # Check if line ends with '{' (ignoring trailing whitespace)
        stripped = line_text.rstrip()
        extra_indent = "    " if stripped.endswith("{") else ""

        self.text.edit_separator()
        self.text.insert("insert", "\n" + base_indent + extra_indent)
        self.text.edit_separator()
        self.text.see("insert")

        self._on_content_change()
        if self.on_edit and not self._ignore_edit_event:
            self.on_edit()
        self.schedule_syntax_highlight()
        return "break"

    def _on_backspace(self, event=None):
        """Delete matching bracket/quote pair if cursor is between them, or delete selection."""
        if self.error_line_num is not None:
            self.clear_highlight()
        self.empty_overlay.place_forget()

        # If there is an active selection, delete selection
        try:
            sel_start = self.text.index("sel.first")
            sel_end = self.text.index("sel.last")
            if sel_start and sel_end and self.text.compare(sel_start, "<", sel_end):
                self.text.edit_separator()
                self.text.delete("sel.first", "sel.last")
                self.text.edit_separator()
                self._on_content_change()
                if self.on_edit and not self._ignore_edit_event:
                    self.on_edit()
                self.schedule_syntax_highlight()
                return "break"
        except tk.TclError:
            pass

        # Feature 4: Backspace Pair Deletion
        if self.text.compare("insert", ">", "1.0"):
            prev_char = self.text.get("insert-1c")
            next_char = self.text.get("insert")
            pairs = {'(': ')', '{': '}', '[': ']', '"': '"', "'": "'"}
            if prev_char in pairs and next_char == pairs[prev_char]:
                self.text.edit_separator()
                self.text.delete("insert-1c", "insert+1c")
                self.text.edit_separator()
                self._on_content_change()
                if self.on_edit and not self._ignore_edit_event:
                    self.on_edit()
                self.schedule_syntax_highlight()
                return "break"

        return None

    def _check_empty_state(self):
        """Show or hide the centered empty-editor welcome state."""
        content = self.get_content().strip()
        if not content:
            self.empty_overlay.place(relx=0.5, rely=0.45, anchor="center")
        else:
            self.empty_overlay.place_forget()

    def _configure_tags(self):
        t = self.theme
        self.text.tag_configure("current_line", background=t["current_line"])
        self.text.tag_configure("error_line", background=t["error_line"], foreground=t["error_line_fg"])
        self.text.tag_configure("syntax_kw", foreground=t.get("syntax_kw", "#569cd6"))
        self.text.tag_configure("syntax_type", foreground=t.get("syntax_type", "#4ec9b0"))
        self.text.tag_configure("syntax_anno", foreground=t.get("syntax_anno", "#dcdcaa"))
        self.text.tag_configure("syntax_str", foreground=t["syntax_str"])
        self.text.tag_configure("syntax_comm", foreground=t["syntax_comm"])
        self.text.tag_configure("syntax_num", foreground=t["syntax_num"])
        self.text.tag_configure("syntax_op", foreground=t.get("syntax_op", "#d4d4d4"))
        self.text.tag_raise("error_line")

        self.line_canvas.tag_configure("gutter_normal", foreground=t["fg_muted"], justify="right")
        self.line_canvas.tag_configure("gutter_current", foreground=t["current_gutter_fg"], justify="right")
        self.line_canvas.tag_configure("gutter_error", foreground=t["gutter_error_fg"], background=t["gutter_error_bg"], justify="right")

    def set_theme(self, theme):
        self.theme = theme
        self.config(bg=theme["bg_main"])
        self.gutter_frame.config(bg=theme["bg_gutter"])
        self.line_canvas.config(
            bg=theme["bg_gutter"],
            fg=theme["fg_muted"],
            selectbackground=theme["bg_gutter"]
        )
        self.separator.config(bg=theme["border"])
        self.v_scrollbar.set_theme(theme)
        self.h_scrollbar.set_theme(theme)
        self.text.config(
            bg=theme["bg_main"],
            fg=theme["fg_main"],
            insertbackground=theme["fg_main"],
            selectbackground="#264f78" if theme == THEMES["dark"] else "#cce8ff",
            selectforeground="#ffffff" if theme == THEMES["dark"] else "#000000"
        )
        self.empty_overlay.config(bg=theme["bg_main"])
        self.empty_title.config(bg=theme["bg_main"], fg=theme["fg_muted"])
        self.empty_sub.config(bg=theme["bg_main"], fg=theme["fg_dim"])
        self.empty_hint.config(bg=theme["bg_main"], fg=theme["fg_dim"])
        self._configure_tags()
        self.schedule_syntax_highlight(immediate=True)
        self.update_line_numbers()
        self._check_empty_state()

    def set_font_size(self, size):
        self.font_size = max(8, min(32, size))
        self.font = ("Consolas", self.font_size)
        self.text.config(font=self.font)
        self.line_canvas.config(font=self.font)
        self.update_line_numbers()

    def _on_v_scroll(self, *args):
        self.text.yview(*args)
        self.line_canvas.yview(*args)

    def _on_h_scroll(self, *args):
        self.text.xview(*args)

    def _on_text_yscroll(self, *args):
        self.v_scrollbar.set(*args)
        try:
            self.line_canvas.yview_moveto(args[0])
        except Exception:
            pass

    def _on_gutter_mousewheel(self, event):
        if event.delta:
            self.text.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def _on_key_press(self, event):
        # Clear error highlight ONLY when actual editing keys are pressed
        non_editing_keys = (
            "Control_L", "Control_R", "Shift_L", "Shift_R", "Alt_L", "Alt_R",
            "Caps_Lock", "Escape", "F1", "F2", "F3", "F4", "F5", "F6", "F7",
            "F8", "F9", "F10", "F11", "F12", "Up", "Down", "Left", "Right",
            "Home", "End", "Prior", "Next"
        )
        if event.keysym not in non_editing_keys and not (event.state & 0x4 and event.keysym in ('c', 'C')):
            if self.error_line_num is not None:
                self.clear_highlight()
            self.empty_overlay.place_forget()

        # Automatic bracket and quote pairing
        if event.char in ('(', '[', '{', '"', "'", ')', ']', '}'):
            # Only handle when Control is not held
            if not (event.state & 0x4):
                res = self._handle_bracket_or_quote(event.char)
                if res == "break":
                    return "break"

    def _handle_bracket_or_quote(self, char):
        self.empty_overlay.place_forget()
        if self.error_line_num is not None:
            self.clear_highlight()

        # Check for active selection
        try:
            sel_start = self.text.index("sel.first")
            sel_end = self.text.index("sel.last")
            has_selection = bool(sel_start and sel_end and self.text.compare(sel_start, "<", sel_end))
        except tk.TclError:
            has_selection = False

        pairs = {
            '(': ')',
            '[': ']',
            '{': '}',
            '"': '"',
            "'": "'"
        }

        # 1. Selection wrapping (Feature 6):
        # If user selects text and types an opening bracket or quote:
        if has_selection:
            if char in pairs:
                close_char = pairs[char]
                sel_text = self.text.get(sel_start, sel_end)
                self.text.edit_separator()
                self.text.delete(sel_start, sel_end)
                self.text.insert(sel_start, char + sel_text + close_char)
                inner_start = f"{sel_start}+1c"
                inner_end = f"{sel_start}+1c+{len(sel_text)}c"
                self.text.tag_add("sel", inner_start, inner_end)
                self.text.mark_set("insert", inner_end)
                self.text.edit_separator()
                self._on_content_change()
                if self.on_edit and not self._ignore_edit_event:
                    self.on_edit()
                self.schedule_syntax_highlight()
                return "break"
            else:
                # User typed a closing bracket while text is selected: normal replace
                self.text.edit_separator()
                self.text.delete(sel_start, sel_end)
                self.text.insert("insert", char)
                self.text.edit_separator()
                self._on_content_change()
                if self.on_edit and not self._ignore_edit_event:
                    self.on_edit()
                self.schedule_syntax_highlight()
                return "break"

        # 2. No selection:
        next_char = self.text.get("insert")
        prev_char = self.text.get("insert-1c") if self.text.compare("insert", ">", "1.0") else ""

        # Feature 3: Smart Closing Character Handling
        # If cursor is immediately before that closing character, step over it!
        if char in (')', ']', '}', '"', "'") and next_char == char:
            self.text.mark_set("insert", "insert+1c")
            self.text.see("insert")
            self._on_content_change()
            return "break"

        # Feature 1: Automatic Bracket Closing ('(', '[', '{')
        if char in ('(', '[', '{'):
            close_char = pairs[char]
            self.text.edit_separator()
            self.text.insert("insert", char + close_char)
            self.text.mark_set("insert", "insert-1c")
            self.text.edit_separator()
            self.text.see("insert")
            self._on_content_change()
            if self.on_edit and not self._ignore_edit_event:
                self.on_edit()
            self.schedule_syntax_highlight()
            return "break"

        # Feature 2: Automatic Quote Pairing ('"', "'")
        if char in ('"', "'"):
            should_pair = True
            if prev_char == '\\':
                should_pair = False
            elif char == "'" and prev_char.isalnum():
                should_pair = False
            else:
                cur_line = self.text.index("insert").split(".")[0]
                line_text_before = self.text.get(f"{cur_line}.0", "insert")
                unescaped_count = 0
                i = 0
                while i < len(line_text_before):
                    if line_text_before[i] == '\\':
                        i += 2
                        continue
                    if line_text_before[i] == char:
                        unescaped_count += 1
                    i += 1
                if unescaped_count % 2 == 1:
                    should_pair = False

            self.text.edit_separator()
            if should_pair:
                self.text.insert("insert", char + char)
                self.text.mark_set("insert", "insert-1c")
            else:
                self.text.insert("insert", char)
            self.text.edit_separator()

            self.text.see("insert")
            self._on_content_change()
            if self.on_edit and not self._ignore_edit_event:
                self.on_edit()
            self.schedule_syntax_highlight()
            return "break"

        # Closing brackets when next_char != char: normal insert
        return None

    def _on_key_release(self, event=None):
        self._on_content_change()
        if not self._ignore_edit_event:
            # Check if actual character was typed/deleted
            if self.on_edit:
                self.on_edit()
        self.schedule_syntax_highlight()
        self._check_empty_state()

    def _on_content_change(self, event=None):
        self.update_line_numbers()
        self._highlight_current_line()
        self._check_empty_state()
        if self.on_cursor_move:
            try:
                line, col = self.text.index("insert").split(".")
                self.on_cursor_move(int(line), int(col) + 1)
            except Exception:
                pass

    def _highlight_current_line(self):
        self.text.tag_remove("current_line", "1.0", "end")
        try:
            cur = self.text.index("insert").split(".")[0]
            self.text.tag_add("current_line", f"{cur}.0", f"{cur}.end+1c")
            self.text.tag_lower("current_line")
        except Exception:
            pass

    def update_line_numbers(self):
        """Re-render line numbers in gutter with right-alignment, dynamic width, and current/error line styling."""
        try:
            lines = int(self.text.index("end-1c").split(".")[0])
        except Exception:
            lines = 1

        try:
            current_line_idx = int(self.text.index("insert").split(".")[0])
        except Exception:
            current_line_idx = 1

        # Calculate required gutter width based on total number of lines
        digits = max(2, len(str(lines)))
        gutter_width = max(4, digits + 2)

        self.line_canvas.config(state="normal", width=gutter_width)
        self.line_canvas.delete("1.0", "end")

        for i in range(1, lines + 1):
            line_str = f"{i:>{digits}}\n" if i < lines else f"{i:>{digits}}"
            start = f"{i}.0"
            self.line_canvas.insert(start, line_str)

            if i == self.error_line_num:
                self.line_canvas.tag_add("gutter_error", f"{i}.0", f"{i}.end")
            elif i == current_line_idx:
                self.line_canvas.tag_add("gutter_current", f"{i}.0", f"{i}.end")
            else:
                self.line_canvas.tag_add("gutter_normal", f"{i}.0", f"{i}.end")

        self.line_canvas.config(state="disabled")

        # Synchronize vertical scroll of gutter with text editor
        try:
            y_top = self.text.yview()[0]
            self.line_canvas.yview_moveto(y_top)
        except Exception:
            pass

    def highlight_error_line(self, line_num):
        """Highlight offending line in editor and gutter, move cursor, and scroll into view."""
        self.clear_highlight()
        if line_num is not None and line_num > 0:
            self.error_line_num = line_num
            start = f"{line_num}.0"
            end = f"{line_num}.end+1c"
            self.text.tag_add("error_line", start, end)
            self.text.tag_raise("error_line")

            # Move cursor to offending line
            self.text.mark_set("insert", start)
            self.text.see(start)
            self._highlight_current_line()
            self.update_line_numbers()
            self._check_empty_state()

            if self.on_cursor_move:
                self.on_cursor_move(line_num, 1)

    def clear_highlight(self):
        """Clear error line highlight tags from editor and gutter."""
        self.error_line_num = None
        self.text.tag_remove("error_line", "1.0", "end")
        self.update_line_numbers()

    def schedule_syntax_highlight(self, immediate=False):
        if self._highlight_job:
            self.after_cancel(self._highlight_job)
            self._highlight_job = None
        if immediate:
            self._apply_syntax_highlight()
        else:
            self._highlight_job = self.after(120, self._apply_syntax_highlight)

    def _apply_syntax_highlight(self):
        self._highlight_job = None
        code = self.get_content()
        if len(code) > 100000:
            return  # Skip huge files for performance

        for tag in ("syntax_kw", "syntax_type", "syntax_anno", "syntax_str", "syntax_comm", "syntax_num", "syntax_op"):
            self.text.tag_remove(tag, "1.0", "end")

        # 1. Comments
        for m in re.finditer(r'//[^\n]*|/\*[\s\S]*?\*/', code):
            start_idx = f"1.0+{m.start()}c"
            end_idx = f"1.0+{m.end()}c"
            self.text.tag_add("syntax_comm", start_idx, end_idx)

        # 2. Strings & Text Blocks & Characters
        for m in re.finditer(r'"""[\s\S]*?"""|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', code):
            start_idx = f"1.0+{m.start()}c"
            end_idx = f"1.0+{m.end()}c"
            self.text.tag_add("syntax_str", start_idx, end_idx)

        # 3. Numbers
        for m in re.finditer(r'\b0[xX][0-9a-fA-F_]+|\b0[bB][01_]+|\b\d[\d_]*(?:\.[\d_]+)?(?:[eE][+-]?\d+)?(?:[fFdDlL])?\b', code):
            start_idx = f"1.0+{m.start()}c"
            end_idx = f"1.0+{m.end()}c"
            self.text.tag_add("syntax_num", start_idx, end_idx)

        # 4. Annotations
        for m in re.finditer(r'@[a-zA-Z_][a-zA-Z0-9_]*', code):
            start_idx = f"1.0+{m.start()}c"
            end_idx = f"1.0+{m.end()}c"
            self.text.tag_add("syntax_anno", start_idx, end_idx)

        # 5. Keywords & Types
        for m in re.finditer(r'\b[a-zA-Z_][a-zA-Z0-9_-]*\b', code):
            word = m.group(0)
            start_idx = f"1.0+{m.start()}c"
            end_idx = f"1.0+{m.end()}c"
            if word in JAVA_TYPES:
                self.text.tag_add("syntax_type", start_idx, end_idx)
            elif word in JAVA_KEYWORDS:
                self.text.tag_add("syntax_kw", start_idx, end_idx)

    def get_content(self):
        return self.text.get("1.0", "end-1c")

    def set_content(self, content):
        self._ignore_edit_event = True
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)
        self.clear_highlight()
        self.text.mark_set("insert", "1.0")
        self.update_line_numbers()
        self._highlight_current_line()
        self.schedule_syntax_highlight(immediate=True)
        self._check_empty_state()
        self._ignore_edit_event = False

    def clear(self):
        self._ignore_edit_event = True
        self.text.delete("1.0", "end")
        self.clear_highlight()
        self.text.mark_set("insert", "1.0")
        self.update_line_numbers()
        self._highlight_current_line()
        self.schedule_syntax_highlight(immediate=True)
        self._check_empty_state()
        self._ignore_edit_event = False


def fuzzy_score(query, target):
    """Subsequence fuzzy match scorer. Returns score > 0 for match, or -1 for no match."""
    query = query.lower().strip()
    target = target.lower().strip()
    if not query:
        return 100
    if query == target:
        return 1000
    if target.startswith(query):
        return 800 - len(target)

    q_idx = 0
    score = 0
    last_match = -1
    consecutive = 0

    for i, ch in enumerate(target):
        if q_idx < len(query) and ch == query[q_idx]:
            q_idx += 1
            if i == 0 or target[i - 1] in " _-./()":
                score += 60  # Word boundary bonus
            if last_match == i - 1:
                consecutive += 1
                score += 25 * consecutive
            else:
                consecutive = 0
            score += 15
            last_match = i

    if q_idx == len(query):
        score += max(0, 100 - len(target))
        return score
    return -1


class CommandPalette(tk.Frame):
    """VS Code-style centered Command Palette overlay (Ctrl+Shift+P / F1)."""

    def __init__(self, parent, commands, theme, on_goto_line=None, on_close=None):
        super().__init__(
            parent,
            bg=theme["palette_bg"],
            highlightthickness=1,
            highlightbackground=theme["palette_border"],
            highlightcolor=theme["palette_border"],
            padx=4,
            pady=4
        )
        self.commands = commands
        self.theme = theme
        self.filtered_items = []
        self.on_goto_line = on_goto_line
        self.on_close = on_close
        self.is_visible = False

        # Header Label
        self.header_lbl = tk.Label(
            self,
            text="TYPE A COMMAND",
            font=("Segoe UI", 8, "bold"),
            bg=theme["palette_bg"],
            fg=theme["fg_muted"],
            anchor="w",
            padx=8,
            pady=2
        )
        self.header_lbl.pack(fill="x")

        # Search Input Container
        input_container = tk.Frame(self, bg=theme["palette_bg"], padx=6, pady=4)
        input_container.pack(fill="x")

        self.prompt_lbl = tk.Label(
            input_container,
            text=">",
            font=("Segoe UI", 11, "bold"),
            bg=theme["palette_input_bg"],
            fg=theme["accent"],
            padx=6
        )
        self.prompt_lbl.pack(side="left", fill="y")

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            input_container,
            textvariable=self.entry_var,
            font=("Segoe UI", 10),
            bg=theme["palette_input_bg"],
            fg=theme["fg_main"],
            insertbackground=theme["fg_main"],
            relief="flat",
            border=0
        )
        self.entry.pack(side="left", fill="both", expand=True, ipady=4)

        # Separator line
        self.sep = tk.Frame(self, bg=theme["border"], height=1)
        self.sep.pack(fill="x", padx=6, pady=(4, 2))

        # Command Listbox
        self.listbox = tk.Listbox(
            self,
            font=("Segoe UI", 10),
            bg=theme["palette_bg"],
            fg=theme["fg_main"],
            selectbackground=theme["palette_sel_bg"],
            selectforeground=theme["palette_sel_fg"],
            relief="flat",
            border=0,
            activestyle="none",
            height=9,
            highlightthickness=0
        )
        self.listbox.pack(fill="both", expand=True, padx=6, pady=4)

        # Bindings
        self.entry.bind("<KeyRelease>", self._on_search_key)
        self.entry.bind("<Down>", self._on_arrow_down)
        self.entry.bind("<Up>", self._on_arrow_up)
        self.entry.bind("<Return>", self._on_execute)
        self.entry.bind("<Escape>", self._on_escape)

        self.listbox.bind("<Return>", self._on_execute)
        self.listbox.bind("<Escape>", self._on_escape)
        self.listbox.bind("<Double-Button-1>", self._on_execute)

    def set_theme(self, theme):
        self.theme = theme
        self.config(
            bg=theme["palette_bg"],
            highlightbackground=theme["palette_border"],
            highlightcolor=theme["palette_border"]
        )
        self.header_lbl.config(bg=theme["palette_bg"], fg=theme["fg_muted"])
        self.prompt_lbl.config(bg=theme["palette_input_bg"], fg=theme["accent"])
        self.entry.config(
            bg=theme["palette_input_bg"],
            fg=theme["fg_main"],
            insertbackground=theme["fg_main"]
        )
        self.sep.config(bg=theme["border"])
        self.listbox.config(
            bg=theme["palette_bg"],
            fg=theme["fg_main"],
            selectbackground=theme["palette_sel_bg"],
            selectforeground=theme["palette_sel_fg"]
        )

    def show(self, initial_query=""):
        self.is_visible = True
        self.entry_var.set(initial_query)
        self._filter_commands(initial_query)
        self.place(relx=0.5, y=36, anchor="n", width=640, height=280)
        self.lift()
        self.entry.focus_set()
        if initial_query:
            self.entry.icursor(len(initial_query))

    def hide(self):
        self.is_visible = False
        self.place_forget()
        if self.on_close:
            self.on_close()

    def _filter_commands(self, query):
        q = query.strip()
        self.filtered_items = []

        if q.startswith(":"):
            line_str = q[1:].strip()
            if line_str.isdigit():
                line_num = int(line_str)
                self.filtered_items.append((
                    f"Go to line {line_num}",
                    f":{line_num}",
                    lambda num=line_num: self.on_goto_line(num) if self.on_goto_line else None
                ))
            else:
                self.filtered_items.append((
                    "Type line number (e.g. :12)",
                    "",
                    None
                ))
        else:
            scored = []
            for name, shortcut, callback in self.commands:
                score = fuzzy_score(q, name)
                if score >= 0:
                    scored.append((score, name, shortcut, callback))

            scored.sort(key=lambda x: x[0], reverse=True)
            self.filtered_items = [(name, shortcut, cb) for _, name, shortcut, cb in scored[:9]]

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, "end")
        for item in self.filtered_items:
            name, shortcut, _ = item
            display_text = f"  {name:<42} {shortcut:>16}"
            self.listbox.insert("end", display_text)
        if self.filtered_items:
            self.listbox.select_set(0)
            self.listbox.activate(0)

    def _on_search_key(self, event=None):
        keysym = getattr(event, "keysym", "")
        if keysym in ("Up", "Down", "Return", "Escape"):
            return
        query = self.entry_var.get()
        self._filter_commands(query)

    def _on_arrow_down(self, event):
        sel = self.listbox.curselection()
        if sel:
            idx = (sel[0] + 1) % max(1, len(self.filtered_items))
        else:
            idx = 0
        self.listbox.selection_clear(0, "end")
        if self.filtered_items:
            self.listbox.selection_set(idx)
            self.listbox.activate(idx)
            self.listbox.see(idx)
        return "break"

    def _on_arrow_up(self, event):
        sel = self.listbox.curselection()
        if sel:
            idx = (sel[0] - 1) % max(1, len(self.filtered_items))
        else:
            idx = max(0, len(self.filtered_items) - 1)
        self.listbox.selection_clear(0, "end")
        if self.filtered_items:
            self.listbox.selection_set(idx)
            self.listbox.activate(idx)
            self.listbox.see(idx)
        return "break"

    def _on_execute(self, event=None):
        sel = self.listbox.curselection()
        if sel and 0 <= sel[0] < len(self.filtered_items):
            item = self.filtered_items[sel[0]]
            callback = item[2]
            self.hide()
            if callable(callback):
                callback()
        return "break"

    def _on_escape(self, event=None):
        self.hide()
        return "break"


class Tooltip:
    """Lightweight hover tooltip for Tkinter widgets."""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        try:
            x = self.widget.winfo_rootx() + 2
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
            self.tip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            tw.attributes("-topmost", True)
            label = tk.Label(
                tw,
                text=self.text,
                justify="left",
                background="#1e1e1e",
                foreground="#e0e0e0",
                relief="solid",
                borderwidth=1,
                highlightthickness=0,
                font=("Segoe UI", 8),
                padx=6,
                pady=2
            )
            label.pack()
        except Exception:
            pass

    def hide_tip(self, event=None):
        if self.tip_window:
            try:
                self.tip_window.destroy()
            except Exception:
                pass
            self.tip_window = None


class ToolbarActionBtn(tk.Frame):
    """Sleek terminal-native icon button with hover glow and tooltip."""

    def __init__(self, parent, icon, tooltip_text, command, is_primary=False, theme=None):
        self.theme = theme or THEMES["dark"]
        self.command = command
        self.is_primary = is_primary
        self.icon_symbol = icon
        self.tooltip_text = tooltip_text

        t = self.theme
        if self.is_primary:
            self.default_bg = "#152218"
            self.default_border = "#00e676"
            self.hover_bg = "#1f3624"
            self.hover_border = "#00ff88"
        else:
            self.default_bg = t["chip_bg"]
            self.default_border = t["border"]
            self.hover_bg = t["chip_hover"]
            self.hover_border = t["accent"] if icon == "⚡" else "#555555"

        super().__init__(
            parent,
            bg=self.default_border,
            highlightthickness=0,
            padx=1,
            pady=1,
            cursor="hand2"
        )

        self.inner = tk.Frame(self, bg=self.default_bg, padx=8, pady=2)
        self.inner.pack(fill="both", expand=True)

        # Icon Label
        icon_fg = "#00ff88" if is_primary else t["accent"] if icon == "⚡" else t["fg_bright"]
        self.icon_lbl = tk.Label(
            self.inner,
            text=icon,
            font=("Segoe UI", 10, "bold"),
            fg=icon_fg,
            bg=self.default_bg
        )
        self.icon_lbl.pack(padx=2, pady=0)

        # Bind click and hover events
        widgets = [self, self.inner, self.icon_lbl]
        for w in widgets:
            w.bind("<Button-1>", lambda e: self._on_click())
            w.bind("<Enter>", lambda e: self._on_enter())
            w.bind("<Leave>", lambda e: self._on_leave())

        # Tooltip
        if tooltip_text:
            self.tooltip = Tooltip(self, tooltip_text)
            self.icon_tooltip = Tooltip(self.icon_lbl, tooltip_text)
            self.inner_tooltip = Tooltip(self.inner, tooltip_text)

    def _on_click(self):
        if callable(self.command):
            self.command()

    def _on_enter(self):
        self.config(bg=self.hover_border)
        self.inner.config(bg=self.hover_bg)
        self.icon_lbl.config(bg=self.hover_bg)

    def _on_leave(self):
        self.config(bg=self.default_border)
        self.inner.config(bg=self.default_bg)
        self.icon_lbl.config(bg=self.default_bg)

    def set_theme(self, t):
        self.theme = t
        if self.is_primary:
            self.default_bg = "#152218"
            self.default_border = "#00e676"
            self.hover_bg = "#1f3624"
            self.hover_border = "#00ff88"
            icon_fg = "#00ff88"
        else:
            self.default_bg = t["chip_bg"]
            self.default_border = t["border"]
            self.hover_bg = t["chip_hover"]
            self.hover_border = t["accent"] if self.icon_symbol == "⚡" else "#555555"
            icon_fg = t["accent"] if self.icon_symbol == "⚡" else t["fg_bright"]

        self.config(bg=self.default_border)
        self.inner.config(bg=self.default_bg)
        self.icon_lbl.config(bg=self.default_bg, fg=icon_fg)


class JavaSyntaxCheckerApp:
    """Main Application Window with Polished Minimal Chrome, Command Palette, and Output Terminal."""

    def __init__(self, root):
        self.root = root
        self.current_filepath = ""
        self.is_dirty = False
        self.last_error_line = None
        self.output_visible = True

        try:
            self.app_icon = tk.PhotoImage(data=APP_ICON_B64)
            self.root.iconphoto(True, self.app_icon)
        except Exception:
            pass

        self.current_theme_name = "dark"
        self.theme = THEMES[self.current_theme_name]
        self.root.configure(bg=self.theme["bg_main"])

        self.backend = ParserBackend()
        self.path_var = tk.StringVar()

        self._build_ui()
        self._setup_command_palette()
        self._bind_shortcuts()
        self._update_title_bar()

        # Initial output welcoming user
        self.log_output("$ ready", "cmd")
        self.log_output("Java 21 Syntax Verification Engine initialized (LALR(1) GNU Bison & Flex).", "normal")

    def _build_ui(self):
        t = self.theme

        # 1. Slim Top Bar
        self.top_bar = tk.Frame(self.root, bg=t["bg_panel"], height=32, padx=10, pady=4)
        self.top_bar.pack(side="top", fill="x")

        # Sleek File Tab Container
        self.tab_frame = tk.Frame(
            self.top_bar,
            bg=t["bg_main"],
            padx=8,
            pady=2,
            highlightthickness=1,
            highlightbackground=t["border"]
        )
        self.tab_frame.pack(side="left")

        self.file_dot = tk.Label(
            self.tab_frame,
            text="",
            font=("Segoe UI", 9, "bold"),
            fg=t["accent_hover"],
            bg=t["bg_main"]
        )
        self.file_dot.pack(side="left", padx=(0, 2))

        self.file_label = tk.Label(
            self.tab_frame,
            text="Untitled.java",
            font=("Segoe UI", 9, "bold"),
            fg=t["fg_bright"],
            bg=t["bg_main"]
        )
        self.file_label.pack(side="left")

        self.tab_close = tk.Label(
            self.tab_frame,
            text="×",
            font=("Segoe UI", 9),
            fg=t["fg_muted"],
            bg=t["bg_main"],
            cursor="hand2",
            padx=4
        )
        self.tab_close.pack(side="left", padx=(4, 0))
        self.tab_close.bind("<Button-1>", lambda e: self.on_close_tab())
        self.tab_close.bind("<Enter>", lambda e: self.tab_close.config(fg=t["fg_bright"]))
        self.tab_close.bind("<Leave>", lambda e: self.tab_close.config(fg=t["fg_muted"]))

        # Right: Action Buttons Group (Only two icon buttons: Palette and Check Syntax)
        self.btn_group = tk.Frame(self.top_bar, bg=t["bg_panel"])
        self.btn_group.pack(side="right")

        # 1. Primary Action: Check Syntax (F5) Icon Button
        self.check_btn = ToolbarActionBtn(
            self.btn_group,
            icon="▶",
            tooltip_text="Check Syntax (F5)",
            command=self.on_check_syntax,
            is_primary=True,
            theme=t
        )
        self.check_btn.pack(side="right", padx=(6, 0))

        # 2. Command Palette Icon Button (Ctrl+Shift+P)
        self.palette_btn = ToolbarActionBtn(
            self.btn_group,
            icon="⚡",
            tooltip_text="Command Palette (Ctrl+Shift+P)",
            command=self.toggle_command_palette,
            is_primary=False,
            theme=t
        )
        self.palette_btn.pack(side="right")

        # Compatibility proxies for unit tests
        self.browse_btn = self.palette_btn
        self.clear_btn = self.palette_btn

        # 1px border line between top bar and editor
        self.sep_top = tk.Frame(self.root, bg=t["border"], height=1)
        self.sep_top.pack(side="top", fill="x")

        # 2. Main Center Area (Editor + Output Panel)
        self.center_paned = tk.PanedWindow(
            self.root,
            orient="vertical",
            bg=t["border"],
            sashwidth=3,
            sashrelief="flat"
        )
        self.center_paned.pack(fill="both", expand=True)

        # Editor Area
        self.editor = LineNumberText(
            self.center_paned,
            theme=t,
            on_cursor_move=self._update_cursor_info,
            on_edit=self._on_editor_modified
        )
        self.center_paned.add(self.editor, minsize=180, stretch="always")

        # Output Terminal Panel (Compact default)
        self.output_frame = tk.Frame(self.center_paned, bg=t["bg_output"])
        self.center_paned.add(self.output_frame, minsize=40, height=80)

        # Output Header
        self.output_header = tk.Frame(self.output_frame, bg=t["bg_panel"], padx=8, pady=2)
        self.output_header.pack(fill="x")

        self.output_title = tk.Label(
            self.output_header,
            text="OUTPUT",
            font=("Segoe UI", 8, "bold"),
            fg=t["fg_muted"],
            bg=t["bg_panel"]
        )
        self.output_title.pack(side="left")

        self.output_controls = tk.Frame(self.output_header, bg=t["bg_panel"])
        self.output_controls.pack(side="right")

        self.output_toggle_btn = tk.Label(
            self.output_controls,
            text="▼",
            font=("Segoe UI", 7),
            fg=t["fg_muted"],
            bg=t["bg_panel"],
            cursor="hand2",
            padx=4
        )
        self.output_toggle_btn.pack(side="left", padx=(0, 4))
        self.output_toggle_btn.bind("<Button-1>", lambda e: self.toggle_output_panel())
        self.output_toggle_btn.bind("<Enter>", lambda e: self.output_toggle_btn.config(fg=t["fg_bright"]))
        self.output_toggle_btn.bind("<Leave>", lambda e: self.output_toggle_btn.config(fg=t["fg_muted"]))

        self.output_clear_btn = tk.Label(
            self.output_controls,
            text="Clear",
            font=("Segoe UI", 8),
            fg=t["fg_muted"],
            bg=t["bg_panel"],
            cursor="hand2",
            padx=4
        )
        self.output_clear_btn.pack(side="left")
        self.output_clear_btn.bind("<Button-1>", lambda e: self.clear_output())
        self.output_clear_btn.bind("<Enter>", lambda e: self.output_clear_btn.config(fg=t["fg_bright"]))
        self.output_clear_btn.bind("<Leave>", lambda e: self.output_clear_btn.config(fg=t["fg_muted"]))

        # Output Text
        self.output_text = tk.Text(
            self.output_frame,
            font=("Consolas", 9),
            bg=t["bg_output"],
            fg=t["fg_main"],
            padx=8,
            pady=4,
            border=0,
            relief="flat",
            state="disabled",
            height=3,
            wrap="none"
        )
        self.output_text.pack(fill="both", expand=True)

        self.output_text.tag_configure("dim", foreground=t["fg_dim"])
        self.output_text.tag_configure("cmd", foreground=t.get("output_cmd_fg", "#858585"), font=("Consolas", 9, "italic"))
        self.output_text.tag_configure("normal", foreground=t["fg_main"])
        self.output_text.tag_configure("success", foreground=t["output_success_fg"], font=("Consolas", 9, "bold"))
        self.output_text.tag_configure("error", foreground=t["output_error_fg"], font=("Consolas", 9, "bold"))
        self.output_text.tag_configure("warn", foreground=t.get("output_warn_fg", "#cca700"))

        # 1px border line above status bar
        self.sep_bot = tk.Frame(self.root, bg=t["border"], height=1)
        self.sep_bot.pack(side="bottom", fill="x")

        # 3. Bottom Status Bar
        self.status_bar = tk.Frame(self.root, bg=t["status_neutral_bg"], height=24, padx=8)
        self.status_bar.pack(side="bottom", fill="x")

        self.result_card = self.status_bar

        self.result_label = tk.Label(
            self.status_bar,
            text="Ready",
            font=("Segoe UI", 9),
            bg=t["status_neutral_bg"],
            fg=t["status_fg"],
            cursor="hand2"
        )
        self.result_label.pack(side="left", pady=2)
        self.result_label.bind("<Button-1>", self._on_status_label_clicked)

        self.status_right = tk.Frame(self.status_bar, bg=t["status_neutral_bg"])
        self.status_right.pack(side="right", fill="y")

        self.cursor_label = tk.Label(
            self.status_right,
            text="Ln 1, Col 1",
            font=("Segoe UI", 8),
            bg=t["status_neutral_bg"],
            fg=t["status_fg"],
            padx=6
        )
        self.cursor_label.pack(side="left")

        self.encoding_label = tk.Label(
            self.status_right,
            text="UTF-8",
            font=("Segoe UI", 8),
            bg=t["status_neutral_bg"],
            fg=t["status_fg"],
            padx=6
        )
        self.encoding_label.pack(side="left")

        self.engine_label = tk.Label(
            self.status_right,
            text="Java 21 · LALR(1)",
            font=("Segoe UI", 8),
            bg=t["status_neutral_bg"],
            fg=t["status_fg"],
            padx=6
        )
        self.engine_label.pack(side="left")

    def _setup_command_palette(self):
        palette_commands = [
            ("Check Syntax", "Ctrl+Enter", self.on_check_syntax),
            ("Open File", "Ctrl+O", self.on_browse),
            ("Open Sample", "", self.on_open_sample),
            ("Check Folder", "", self.on_check_folder),
            ("New File", "Ctrl+N", self.on_new_file),
            ("Save", "Ctrl+S", self.on_save),
            ("Save As", "Ctrl+Shift+S", self.on_save_as),
            ("Clear Editor", "Ctrl+L", self.on_clear),
            ("Go to Line", "Ctrl+G", self.on_go_to_line_prompt),
            ("Go to Error Line", "F8", self.on_go_to_error_line),
            ("Toggle Output Panel", "Ctrl+J", self.toggle_output_panel),
            ("Clear Output", "", self.clear_output),
            ("Toggle Theme", "", self.toggle_theme),
            ("Zoom In", "Ctrl+=", lambda: self.editor.set_font_size(self.editor.font_size + 1)),
            ("Zoom Out", "Ctrl+-", lambda: self.editor.set_font_size(self.editor.font_size - 1)),
            ("Zoom Reset", "Ctrl+0", lambda: self.editor.set_font_size(11)),
            ("Parser Info", "", self.show_parser_info),
            ("Keyboard Shortcuts", "", self.show_shortcuts_info),
            ("Quit", "Ctrl+Q", self.on_quit)
        ]
        self.command_palette = CommandPalette(
            self.root,
            commands=palette_commands,
            theme=self.theme,
            on_goto_line=self.go_to_line,
            on_close=lambda: self.editor.text.focus_set()
        )

    def _bind_shortcuts(self):
        widgets = [self.root, self.editor.text]

        for w in widgets:
            w.bind("<Control-Shift-P>", lambda e: (self.toggle_command_palette(), "break")[1])
            w.bind("<Control-Shift-p>", lambda e: (self.toggle_command_palette(), "break")[1])
            w.bind("<F1>", lambda e: (self.toggle_command_palette(), "break")[1])
            w.bind("<Control-Return>", lambda e: (self.on_check_syntax(), "break")[1])
            w.bind("<F5>", lambda e: (self.on_check_syntax(), "break")[1])
            w.bind("<Control-o>", lambda e: (self.on_browse(), "break")[1])
            w.bind("<Control-O>", lambda e: (self.on_browse(), "break")[1])
            w.bind("<Control-n>", lambda e: (self.on_new_file(), "break")[1])
            w.bind("<Control-N>", lambda e: (self.on_new_file(), "break")[1])
            w.bind("<Control-s>", lambda e: (self.on_save(), "break")[1])
            w.bind("<Control-S>", lambda e: (self.on_save(), "break")[1])
            w.bind("<Control-Shift-S>", lambda e: (self.on_save_as(), "break")[1])
            w.bind("<Control-Shift-s>", lambda e: (self.on_save_as(), "break")[1])
            w.bind("<Control-l>", lambda e: (self.on_clear(), "break")[1])
            w.bind("<Control-L>", lambda e: (self.on_clear(), "break")[1])
            w.bind("<Control-g>", lambda e: (self.on_go_to_line_prompt(), "break")[1])
            w.bind("<Control-G>", lambda e: (self.on_go_to_line_prompt(), "break")[1])
            w.bind("<F8>", lambda e: (self.on_go_to_error_line(), "break")[1])
            w.bind("<Control-j>", lambda e: (self.toggle_output_panel(), "break")[1])
            w.bind("<Control-J>", lambda e: (self.toggle_output_panel(), "break")[1])
            w.bind("<Control-equal>", lambda e: (self.editor.set_font_size(self.editor.font_size + 1), "break")[1])
            w.bind("<Control-plus>", lambda e: (self.editor.set_font_size(self.editor.font_size + 1), "break")[1])
            w.bind("<Control-minus>", lambda e: (self.editor.set_font_size(self.editor.font_size - 1), "break")[1])
            w.bind("<Control-0>", lambda e: (self.editor.set_font_size(11), "break")[1])
            w.bind("<Control-q>", lambda e: (self.on_quit(), "break")[1])
            w.bind("<Control-Q>", lambda e: (self.on_quit(), "break")[1])

        self.root.bind("<Escape>", lambda e: self.close_command_palette())
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)

    def toggle_command_palette(self, initial_query=""):
        if self.command_palette.is_visible:
            self.command_palette.hide()
        else:
            self.command_palette.show(initial_query)

    def close_command_palette(self):
        if self.command_palette.is_visible:
            self.command_palette.hide()

    def _update_cursor_info(self, line, col):
        self.cursor_label.config(text=f"Ln {line}, Col {col}")

    def _on_editor_modified(self):
        if not self.is_dirty:
            self.is_dirty = True
            self._update_title_bar()

    def _update_title_bar(self):
        name = os.path.basename(self.current_filepath) if self.current_filepath else "Untitled.java"
        if self.is_dirty:
            self.file_dot.config(text="●")
            self.file_label.config(text=name)
            self.root.title(f"Java Syntax Checker - {name} *")
        else:
            self.file_dot.config(text="")
            self.file_label.config(text=name)
            self.root.title(f"Java Syntax Checker - {name}")

    def on_close_tab(self):
        """Close active editor tab / reset buffer."""
        self.on_new_file()

    def log_output(self, text, tag="normal"):
        self.output_text.config(state="normal")
        self.output_text.insert("end", text + "\n", tag)
        self.output_text.see("end")
        self.output_text.config(state="disabled")

    def clear_output(self):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.config(state="disabled")

    def toggle_output_panel(self):
        if self.output_visible:
            self.center_paned.remove(self.output_frame)
            self.output_visible = False
            self.output_toggle_btn.config(text="▲")
        else:
            self.center_paned.add(self.output_frame, minsize=40, height=80)
            self.output_visible = True
            self.output_toggle_btn.config(text="▼")

    def toggle_theme(self):
        self.current_theme_name = "light" if self.current_theme_name == "dark" else "dark"
        self.theme = THEMES[self.current_theme_name]
        t = self.theme

        self.root.config(bg=t["bg_main"])
        self.top_bar.config(bg=t["bg_panel"])
        self.tab_frame.config(bg=t["bg_main"], highlightbackground=t["border"])
        self.file_dot.config(bg=t["bg_main"], fg=t["accent_hover"])
        self.file_label.config(bg=t["bg_main"], fg=t["fg_bright"])
        self.tab_close.config(bg=t["bg_main"], fg=t["fg_muted"])
        self.btn_group.config(bg=t["bg_panel"])
        self.check_btn.set_theme(t)
        self.palette_btn.set_theme(t)
        self.sep_top.config(bg=t["border"])
        self.sep_bot.config(bg=t["border"])
        self.center_paned.config(bg=t["border"])

        self.editor.set_theme(t)
        self.command_palette.set_theme(t)

        self.output_frame.config(bg=t["bg_output"])
        self.output_header.config(bg=t["bg_panel"])
        self.output_title.config(bg=t["bg_panel"], fg=t["fg_muted"])
        self.output_controls.config(bg=t["bg_panel"])
        self.output_toggle_btn.config(bg=t["bg_panel"], fg=t["fg_muted"])
        self.output_clear_btn.config(bg=t["bg_panel"], fg=t["fg_muted"])
        self.output_text.config(bg=t["bg_output"], fg=t["fg_main"])
        self.output_text.tag_configure("dim", foreground=t["fg_dim"])
        self.output_text.tag_configure("cmd", foreground=t.get("output_cmd_fg", "#858585"))
        self.output_text.tag_configure("normal", foreground=t["fg_main"])
        self.output_text.tag_configure("success", foreground=t["output_success_fg"])
        self.output_text.tag_configure("error", foreground=t["output_error_fg"])
        self.output_text.tag_configure("warn", foreground=t.get("output_warn_fg", "#cca700"))

        self._set_status_bar_theme()

    def _set_status_bar_theme(self, state="neutral"):
        t = self.theme
        if state == "success":
            bg = t["status_success_bg"]
        elif state == "error":
            bg = t["status_error_bg"]
        else:
            bg = t["status_neutral_bg"]

        self.status_bar.config(bg=bg)
        self.result_label.config(bg=bg, fg=t["status_fg"])
        self.status_right.config(bg=bg)
        self.cursor_label.config(bg=bg, fg=t["status_fg"])
        self.encoding_label.config(bg=bg, fg=t["status_fg"])
        self.engine_label.config(bg=bg, fg=t["status_fg"])

    def on_check_syntax(self):
        """Always parses the text currently in the editor, not the file on disk."""
        content = self.editor.get_content()
        target_name = os.path.basename(self.current_filepath) if self.current_filepath else "Untitled.java"

        self.log_output(f"$ check {target_name}", "dim")

        if not content.strip():
            msg = "ERROR: Source code editor is empty."
            self.set_result_error(msg)
            self.log_output(msg, "error")
            return

        ret, raw_msg, err_line = self.backend.check_code_string(content)

        if ret == 0:
            success_msg = "Parsing Successful: No syntax errors detected."
            self.set_result_success(success_msg)
            self.log_output(success_msg, "success")
            self.editor.clear_highlight()
            self.last_error_line = None
        else:
            self.last_error_line = err_line
            error_line_str = str(err_line) if err_line is not None else "?"
            error_msg = f"Syntax Error detected at line {error_line_str}"
            self.set_result_error(error_msg)
            self.log_output(error_msg, "error")
            if err_line is not None:
                self.editor.highlight_error_line(err_line)

    def set_result_success(self, msg):
        self._set_status_bar_theme("success")
        self.result_label.config(
            text=msg,
            font=("Segoe UI", 9, "bold")
        )

    def set_result_error(self, msg):
        self._set_status_bar_theme("error")
        self.result_label.config(
            text=msg,
            font=("Segoe UI", 9, "bold")
        )

    def set_result_neutral(self, msg):
        self._set_status_bar_theme("neutral")
        self.result_label.config(
            text=msg,
            font=("Segoe UI", 9)
        )

    def _on_status_label_clicked(self, event=None):
        if self.last_error_line is not None:
            self.go_to_line(self.last_error_line)

    def on_go_to_error_line(self):
        if self.last_error_line is not None:
            self.go_to_line(self.last_error_line)
        else:
            self.log_output("No error line recorded.", "dim")

    def on_go_to_line_prompt(self):
        self.toggle_command_palette(initial_query=":")

    def go_to_line(self, line_num):
        try:
            total_lines = int(self.editor.text.index("end-1c").split(".")[0])
            line_num = max(1, min(total_lines, int(line_num)))
            pos = f"{line_num}.0"
            self.editor.text.mark_set("insert", pos)
            self.editor.text.see(pos)
            self.editor.text.focus_set()
            self.editor._on_content_change()
            self.log_output(f"$ goto line {line_num}", "dim")
        except Exception as e:
            self.log_output(f"Could not jump to line: {e}", "dim")

    def _check_unsaved_changes(self):
        """Ask before discarding unsaved changes."""
        if self.is_dirty:
            res = messagebox.askyesnocancel(
                "Unsaved Changes",
                "Do you want to save changes before continuing?",
                parent=self.root
            )
            if res is True:  # Yes -> Save
                return self.on_save()
            elif res is False:  # No -> Discard
                return True
            else:  # Cancel
                return False
        return True

    def on_new_file(self):
        if not self._check_unsaved_changes():
            return
        self.current_filepath = ""
        self.path_var.set("")
        self.is_dirty = False
        self.last_error_line = None
        self.editor.clear()
        self._update_title_bar()
        self.set_result_neutral("Ready")
        self.log_output("$ new file", "dim")

    def on_browse(self):
        if not self._check_unsaved_changes():
            return

        filepath = filedialog.askopenfilename(
            title="Open Java File",
            filetypes=[("Java Source Files", "*.java"), ("All Files", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            self.current_filepath = filepath
            self.path_var.set(filepath)
            self.is_dirty = False
            self.last_error_line = None
            self.editor.set_content(content)
            self._update_title_bar()
            self.set_result_neutral("Ready")
            self.log_output(f"$ open {os.path.basename(filepath)}", "dim")
        except Exception as e:
            messagebox.showerror("File Error", f"Could not read file:\n{str(e)}")

    def on_open_sample(self):
        """Quickly browse and open test/sample Java files."""
        samples_dir = os.path.join(BASE_DIR, "tests")
        if not os.path.exists(samples_dir):
            samples_dir = BASE_DIR

        files = [f for f in os.listdir(samples_dir) if f.endswith(".java")]
        if not files:
            messagebox.showinfo("Samples", "No sample .java files found in tests directory.")
            return

        sample_commands = []
        for fn in sorted(files):
            full_p = os.path.join(samples_dir, fn)
            sample_commands.append((
                fn,
                "Sample",
                lambda p=full_p: self._load_file_direct(p)
            ))

        sub_palette = CommandPalette(
            self.root,
            commands=sample_commands,
            theme=self.theme,
            on_close=lambda: self.editor.text.focus_set()
        )
        sub_palette.show()

    def _load_file_direct(self, filepath):
        if not self._check_unsaved_changes():
            return
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            self.current_filepath = filepath
            self.path_var.set(filepath)
            self.is_dirty = False
            self.last_error_line = None
            self.editor.set_content(content)
            self._update_title_bar()
            self.set_result_neutral("Ready")
            self.log_output(f"$ open {os.path.basename(filepath)}", "dim")
        except Exception as e:
            messagebox.showerror("File Error", f"Could not read file:\n{str(e)}")

    def on_check_folder(self):
        """Runs the parser over every .java file in a chosen folder and prints a summary."""
        folder = filedialog.askdirectory(title="Select Folder with Java Files")
        if not folder:
            return

        java_files = []
        for root_dir, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root_dir, file))

        if not java_files:
            self.log_output(f"No .java files found in {folder}", "dim")
            return

        self.log_output(f"$ check folder '{folder}' ({len(java_files)} files)", "dim")
        passed = 0
        failed = 0

        for fpath in sorted(java_files):
            rel_name = os.path.relpath(fpath, folder)
            ret, _, err_line = self.backend.check_file(fpath)
            if ret == 0:
                passed += 1
                self.log_output(f"  [PASS] {rel_name}", "success")
            else:
                failed += 1
                self.log_output(f"  [FAIL] {rel_name} (Line {err_line})", "error")

        summary = f"Summary: {passed} passed, {failed} failed out of {len(java_files)} total files."
        self.log_output(summary, "normal")

    def on_save(self):
        if not self.current_filepath:
            return self.on_save_as()

        try:
            content = self.editor.get_content()
            with open(self.current_filepath, "w", encoding="utf-8") as f:
                f.write(content)
            self.is_dirty = False
            self._update_title_bar()
            self.log_output(f"$ save {os.path.basename(self.current_filepath)}", "dim")
            return True
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save file:\n{str(e)}")
            return False

    def on_save_as(self):
        filepath = filedialog.asksaveasfilename(
            title="Save Java Source File",
            defaultextension=".java",
            filetypes=[("Java Source Files", "*.java"), ("All Files", "*.*")]
        )
        if not filepath:
            return False

        self.current_filepath = filepath
        self.path_var.set(filepath)
        return self.on_save()

    def on_clear(self):
        self.editor.clear()
        self.is_dirty = False
        self.last_error_line = None
        self._update_title_bar()
        self.set_result_neutral("Ready")
        self.log_output("$ clear editor", "dim")

    def show_parser_info(self):
        engine_type = "Native shared library (javacheck.dll via ctypes)" if self.backend.use_dll else "Standalone CLI (javacheck.exe)"
        info = f"Java Syntax Checker v21.0\nParser: GNU Bison 3.8.x LALR(1)\nLexer: GNU Flex 2.6.x\nTarget: Java 21 LTS\nEngine: {engine_type}"
        self.log_output(info, "normal")
        messagebox.showinfo("Parser Info", info)

    def show_shortcuts_info(self):
        shortcuts_text = (
            "Keyboard Shortcuts:\n\n"
            "  Ctrl+Shift+P / F1  : Command Palette\n"
            "  Ctrl+Enter / F5    : Check Syntax\n"
            "  Ctrl+O             : Open Java File\n"
            "  Ctrl+N             : New File\n"
            "  Ctrl+S             : Save File\n"
            "  Ctrl+Shift+S       : Save As\n"
            "  Ctrl+L             : Clear Editor\n"
            "  Ctrl+G             : Go to Line (:line)\n"
            "  F8                 : Go to Error Line\n"
            "  Ctrl+J             : Toggle Output Panel\n"
            "  Ctrl+= / Ctrl+-    : Zoom In / Out\n"
            "  Ctrl+0             : Zoom Reset\n"
            "  Ctrl+Q             : Quit"
        )
        self.log_output(shortcuts_text, "dim")
        messagebox.showinfo("Keyboard Shortcuts", shortcuts_text)

    def on_quit(self):
        if not self._check_unsaved_changes():
            return
        self.root.destroy()


def main():
    root = tk.Tk()
    app = JavaSyntaxCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
