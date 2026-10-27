# Java 21 Syntax Checker — Quick Faculty Presentation Sheet

> **Quick Summary Sheet:** Read this in 3 minutes to understand the entire project and explain it to your faculty with confidence.


---

## 1. What is this project? (In 30 Seconds)
We built a **Syntax Checker for Java 21** from scratch using fundamental **Compiler Design** tools (**Flex** and **Bison**).
- **Like the syntax validator in VS Code:** It checks if a `.java` file follows official Java 21 grammar rules.
- **Valid code:** Shows a green **"Valid Syntax"** message.
- **Invalid code:** Pinpoints the exact line number, highlights the line in **red**, marks the line number in the gutter, and scrolls directly to it.
- **Academic Scope:** It is a **front-end syntax checker** (Lexer + Parser). It does *not* do type checking, compile to `.class` bytecode, or run Java code.

---

## 2. Tech Stack at a Glance

| Component | Technology | Why We Used It (What to tell Faculty) |
|---|---|---|
| **Lexer (Scanner)** | **GNU Flex 2.6** | Uses a **DFA** (Deterministic Finite Automaton) to convert raw Java characters into tokens (`class`, `record`, `;`, etc.) and tracks line numbers. |
| **Parser** | **GNU Bison 3.8** | Uses an **LALR(1)** shift-reduce pushdown automaton to verify the token stream against the Java 21 Context-Free Grammar. |
| **C Backend** | **GCC (MinGW)** | Compiles the Lexer and Parser into a fast native Windows shared library (`javacheck.dll`) and CLI tool (`javacheck.exe`). |
| **Desktop GUI** | **Python Tkinter** | Clean dark-mode IDE with line numbers, error highlighting, and Command Palette (`Ctrl+Shift+P`). Zero external dependencies. |
| **Bridge (FFI)** | **Python `ctypes`** | Loads `javacheck.dll` directly into memory so Python calls C in sub-milliseconds without slow process spawning. |

---

## 3. How It Works (The 4-Step Workflow)

```text
[ Java Code in GUI ]
         │
         ▼  (1. Python calls javacheck.dll in-memory via ctypes)
[ GNU Flex Lexer (DFA) ]
         │  (2. Scans code into tokens & tracks line numbers via YY_USER_ACTION)
         ▼
[ GNU Bison Parser (LALR(1)) ]
         │  (3. Checks tokens against Java 21 grammar rules via Shift/Reduce)
         ▼
[ Result Return Code ]
    ├── Code 0 (Success) ──► GUI turns Green: "Valid Java Syntax"
    └── Code 1 (Error)   ──► GUI turns Red: Highlights exact Line N in editor
```

1. **User Action:** User clicks **Check Syntax** (or presses `F5` / `Ctrl+Enter`).
2. **Lexical Analysis (Flex):** Converts code into a token stream. A custom macro (`YY_USER_ACTION`) tracks the exact line and column of every token.
3. **Syntax Analysis (Bison):** Matches tokens against the Java 21 grammar rules. If a token violates grammar, Bison calls `yyerror()` and captures `error_line`.
4. **Visual Display:** If valid, the GUI displays a green status badge. If invalid, the GUI highlights the offending line in red and scrolls to it.

---

## 4. Modern Java 21 Features Supported
Unlike basic classroom parsers that only support Java 7, our grammar handles modern **Java 21 LTS** syntax:
1. **Record Patterns:** `if (obj instanceof Point(var x, var y))`
2. **Pattern Matching for Switch:** `case Point(x, y) when x > 0 -> ...`
3. **Sealed Classes:** `sealed class Shape permits Circle, Square`
4. **Text Blocks:** Multi-line strings `"""..."""`
5. **Local Type Inference:** `var list = new ArrayList<String>();`

---

## 5. What to Say to the Faculty (30-Second Script)

> *"Good morning professors. Our project is a **Java 21 Syntax Checker** implementing a formal compiler front-end.*  
> *We wrote the lexical analyzer in **GNU Flex** and the syntax parser in **GNU Bison** using an **LALR(1) Shift-Reduce state machine** that implements the Java 21 Context-Free Grammar.*  
> *The parser is compiled into a native C shared library (`javacheck.dll`) and connected to a **Python Tkinter GUI** via in-memory `ctypes`.*  
> *When code is checked, it verifies grammar conformity, reports exact error line numbers with red highlighting, and has a 100% pass rate across our 59 automated test cases."*

---

## 6. Top 5 Faculty Questions & 1-Line Answers

**Q1: What parsing algorithm does Bison use here?**  
> **Answer:** **LALR(1)** (Look-Ahead LR with 1-token lookahead). It is a bottom-up shift-reduce algorithm that naturally handles left-recursion and operator precedence.

**Q2: How does the parser know the exact line number of an error?**  
> **Answer:** Flex uses the `YY_USER_ACTION` hook to continuously record `yylineno` into `yylloc`. When Bison encounters an invalid token, `yyerror()` reads `yylloc.first_line`.

**Q3: How does Python talk to the C parser?**  
> **Answer:** Using Python's built-in `ctypes` library, which loads `javacheck.dll` directly into RAM and calls `check_syntax()` with zero subprocess overhead.

**Q4: How did you resolve the "Dangling Else" grammar conflict?**  
> **Answer:** Using Bison's `%nonassoc` precedence directives to give `ELSE` higher precedence, forcing the parser to shift and bind `else` to the innermost `if`.

**Q5: Is this a full Java compiler?**  
> **Answer:** No. It is strictly a **front-end syntax checker**. It does not perform semantic type checking, bytecode generation, or program execution.

---

## 7. Quick 1-Minute Live Demo Steps
1. Run `python gui/app.py`.
2. Type or paste valid Java 21 code with a record:
   ```java
   public class Test { public record Point(int x, int y) {} }
   ```
   Press **`F5`** $\rightarrow$ Show the **Green Success** status badge.
3. Remove the closing brace `}` and press **`F5`** $\rightarrow$ Show the **Red Error** status and the highlighted error line.
4. Show the automated test suite in the terminal:
   ```bash
   python tests/run_tests.py
   ```
   Show them the **59 / 59 Passed (100%)** summary.
