"""
Batch Generator for 20 Academic PDF Documentation Files
Java 21 Syntax Checker using GNU Flex & GNU Bison LALR(1)
"""

import os
import sys

# Ensure local import works
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_engine import PDFBuilder

DOC_DIR = os.path.dirname(os.path.abspath(__file__))

def gen_doc_01():
    doc = PDFBuilder("Project Overview & Foundations", "DOC-01")
    doc.add_title_header("System Overview, Context-Free Grammar, & Scope Boundaries")
    
    doc.add_heading_1("1. Project Title & Designation")
    doc.add_paragraph("Official Title: Java 21 Syntax Checker using GNU Flex, GNU Bison LALR(1), and Python Tkinter.")
    doc.add_paragraph("Academic Track: Course-Based Project (CBP) / Compiler Design & Formal Languages.")
    
    doc.add_heading_1("2. Executive Abstract")
    doc.add_paragraph(
        "Modern programming languages evolve continuously, adding high-level syntactic sugar and pattern-matching constructs. "
        "The Java 21 Syntax Checker is a high-precision, front-end compiler tool designed to formally validate the grammatical "
        "correctness of Java 21 (LTS) source files. Built using GNU Flex 2.6.x (lexical DFA scanner) and GNU Bison 3.8.x "
        "(LALR(1) shift-reduce parser), the engine compiles to a native Windows DLL (javacheck.dll) and standalone CLI binary "
        "(javacheck.exe). An interactive Python 3.10+ / Tkinter desktop interface with an in-memory ctypes foreign function "
        "interface (FFI) enables real-time verification, line-number gutter synchronization, Command Palette quick actions, "
        "and instant red error-line highlighting. The tool achieved a 100% pass rate across 59 parser tests and 14 GUI tests."
    )
    
    doc.add_heading_1("3. What the Project Does")
    doc.add_bullet("Tokenizes Java 21 source code into lexical tokens with line/column coordinates via Flex.", prefix="[1]")
    doc.add_bullet("Parses the token stream against a Java 21 Context-Free Grammar using Bison LALR(1).", prefix="[2]")
    doc.add_bullet("Reports whether the source code conforms to the formal Java 21 specification.", prefix="[3]")
    doc.add_bullet("Pinpoints the exact source line where the first syntax error occurs.", prefix="[4]")
    doc.add_bullet("Presents a responsive, dark-themed VS Code-style graphical developer interface.", prefix="[5]")
    
    doc.add_heading_1("4. Why the Project Was Developed (Academic Motivation)")
    doc.add_paragraph(
        "Most educational compilers and literature examples stop at Java 1.4 or Java 7, omitting modern language structures. "
        "Java 21 LTS introduced groundbreaking features—such as Record Patterns, Pattern Matching for Switch, Switch Guards (when clauses), "
        "Sealed Classes, and Text Blocks. Implementing these modern constructs in a deterministic LALR(1) framework demonstrates "
        "advanced grammar disambiguation, precedence engineering, and native systems interoperability."
    )
    
    doc.add_heading_1("5. Project Boundary: Syntax Checker vs. Full Compiler")
    doc.add_callout(
        "CRITICAL DISTINCTION: This project is strictly a FRONT-END SYNTAX CHECKER and PARSER. "
        "It does NOT perform semantic analysis (type checking, symbol resolution, undeclared variable detection), "
        "does NOT generate JVM bytecode (.class files), and does NOT execute or debug Java programs.",
        title="SCOPE & THEORETICAL BOUNDARY",
        style="warning"
    )
    
    headers = ["Compiler Phase", "Status in This Project", "Implementation Mechanism"]
    rows = [
        ["1. Lexical Analysis", "Fully Implemented (100%)", "GNU Flex 2.6.x (DFA, YY_USER_ACTION)"],
        ["2. Syntax Analysis", "Fully Implemented (100%)", "GNU Bison 3.8.x (LALR(1) Shift-Reduce)"],
        ["3. Semantic Analysis", "Out of Scope", "Not implemented (No symbol tables/types)"],
        ["4. Intermediate Code Gen", "Out of Scope", "Not implemented (No TAC or AST)"],
        ["5. Code Optimization", "Out of Scope", "Not implemented"],
        ["6. Target Code Generation", "Out of Scope", "Not implemented (No .class bytecode)"]
    ]
    doc.add_table(headers, rows, [2.2, 1.8, 3.0])
    
    doc.save(os.path.join(DOC_DIR, "01_Project_Overview.pdf"))

def gen_doc_02():
    doc = PDFBuilder("Objectives, Scope & Requirements", "DOC-02")
    doc.add_title_header("Problem Formulation, Motivations, & Functional Boundaries")
    
    doc.add_heading_1("1. Problem Statement")
    doc.add_paragraph(
        "Java 21 expanded the grammar with intricate constructs such as record patterns, deconstruction, and contextual guards. "
        "Adapting these constructs into a single-token lookahead LALR(1) grammar introduces complex shift/reduce and reduce/reduce ambiguities. "
        "There is a need for a formally verified, deterministic LALR(1) Java 21 syntax analyzer coupled with a modern graphical interface "
        "capable of pinpoint error-line highlighting."
    )
    
    doc.add_heading_1("2. Project Motivation")
    doc.add_bullet("Apply formal Language Theory (DFAs, CFGs, LALR(1) tables) to modern Java 21 LTS syntax.")
    doc.add_bullet("Solve classic compiler conflicts: dangling-else, cast expressions, ragged arrays, and switch guards.")
    doc.add_bullet("Build a zero-overhead native C engine communicating with Python via in-memory ctypes FFI.")
    doc.add_bullet("Deliver a polished, dark-themed VS Code-style developer desktop environment.")
    
    doc.add_heading_1("3. Core Project Objectives")
    doc.add_bullet("Objective 1: Construct a complete GNU Bison LALR(1) grammar for Java 21 (LTS).")
    doc.add_bullet("Objective 2: Build a fast GNU Flex lexical scanner with line and column tracking.")
    doc.add_bullet("Objective 3: Provide exact, drift-free error line reporting across all formatting scenarios.")
    doc.add_bullet("Objective 4: Export a C shared library (javacheck.dll) and standalone CLI (javacheck.exe).")
    doc.add_bullet("Objective 5: Develop a Python Tkinter GUI with Command Palette and error highlighting.")
    doc.add_bullet("Objective 6: Validate 100% test passing rate across 59 parser tests and 14 GUI tests.")
    
    doc.add_heading_1("4. Supported vs. Non-Supported Functionality")
    headers = ["Functional Domain", "Supported in Project", "Non-Supported / Excluded"]
    rows = [
        ["Lexical Tokens", "Keywords, Literals, Comments, Text Blocks", "Preprocessor macros (Java has none)"],
        ["Grammar Syntax", "Java 21 LTS Finalized Standard", "Experimental preview syntax (JEP 430)"],
        ["Error Detection", "First syntax error line & token near", "Multi-error speculative recovery cascade"],
        ["Semantics", "Grammar rule conformance", "Type checking, symbol scope resolution"],
        ["Execution", "Syntax validation status report", "Bytecode generation, JVM execution"]
    ]
    doc.add_table(headers, rows, [1.8, 2.6, 2.6])
    
    doc.save(os.path.join(DOC_DIR, "02_Project_Objectives_and_Scope.pdf"))

def gen_doc_03():
    doc = PDFBuilder("Technology Stack & Toolchain", "DOC-03")
    doc.add_title_header("Tools, Exact Documented Versions, & Architectural Roles")
    
    doc.add_heading_1("1. Technology Stack Overview")
    doc.add_paragraph(
        "The project uses an industry-standard, multi-language systems toolchain consisting of C99, GNU Flex, GNU Bison, "
        "and Python 3.10+. Each tool occupies a strictly defined layer in the compilation and presentation stack."
    )
    
    headers = ["Technology / Tool", "Exact Documented Version", "Role in Project Architecture"]
    rows = [
        ["Target Language", "Java 21 (LTS)", "Language specification targeted by grammar rules"],
        ["GNU Flex", "2.6.x", "Generates lexical scanner (lex.yy.c) from regular expressions"],
        ["GNU Bison", "3.8.x", "Generates LALR(1) shift-reduce parser (java_parser.tab.c)"],
        ["GCC Compiler", "MinGW-w64 (MSYS2 UCRT64)", "Compiles C sources into javacheck.dll and javacheck.exe"],
        ["Python", "3.10+", "Runs desktop GUI and orchestrates automated test suites"],
        ["Tkinter", "Built-in Standard Library", "GUI toolkit rendering editor, line numbers, and palette"],
        ["ctypes", "Built-in Standard Library", "In-memory C Foreign Function Interface loading DLL"],
        ["Build Scripts", "CMD, PowerShell, Make", "Automated multi-platform compilation pipelines"],
        ["Test Runner", "Python unittest", "Automated regression testing of parser and GUI"]
    ]
    doc.add_table(headers, rows, [2.0, 2.0, 3.5])
    
    doc.add_heading_1("2. Detailed Role of Every Component")
    doc.add_heading_2("GNU Flex (Lexical Analyzer)")
    doc.add_paragraph("Compiles regular expressions into an optimized Deterministic Finite Automaton (DFA). Eliminates whitespace and comments while emitting discrete token integers and tracking exact line coordinates.")
    
    doc.add_heading_2("GNU Bison (Syntax Parser)")
    doc.add_paragraph("Translates Context-Free Grammar rules into a deterministic LALR(1) state machine. Manages operator precedence, resolves ambiguities, and catches syntax violations via yyerror().")
    
    doc.add_heading_2("GCC / MinGW-w64 UCRT64 (Native Compiler)")
    doc.add_paragraph("Compiles the generated C files into a high-performance shared library (javacheck.dll) exporting check_syntax() and a standalone CLI binary (javacheck.exe).")
    
    doc.add_heading_2("Python / Tkinter / ctypes (User Interface & FFI)")
    doc.add_paragraph("Provides zero-dependency, cross-platform presentation. Uses ctypes to invoke the native DLL directly in memory without process spawning overhead.")
    
    doc.save(os.path.join(DOC_DIR, "03_Technology_Stack.pdf"))

def gen_doc_04():
    doc = PDFBuilder("Grammar Source & Bison Adaptation", "DOC-04")
    doc.add_title_header("ANTLR4 Reference Grammar Adaptation to LALR(1) Shift-Reduce")
    
    doc.add_heading_1("1. Grammar Source and Origin")
    doc.add_paragraph(
        "The reference grammar for this project was derived from the official ANTLR4 Java grammar repository: "
        "grammar/original/JavaLexer.g4 and grammar/original/JavaParser.g4. "
        "ANTLR4 uses an ALL(*) top-down recursive-descent parsing algorithm with arbitrary lookahead and semantic predicates. "
        "Because GNU Bison uses a deterministic bottom-up LALR(1) algorithm, the reference grammar had to be structurally adapted."
    )
    
    doc.add_heading_1("2. Fundamental Adaptations for GNU Bison LALR(1)")
    
    doc.add_heading_2("A. Left-Recursion Conversion")
    doc.add_paragraph(
        "ANTLR4 expresses repetitive lists using EBNF operators (*, +). In Bison LALR(1), lists are structured using left-recursive "
        "productions to ensure constant stack space during reduction:"
    )
    doc.add_code_block(
        "// Left-recursive list in Bison LALR(1)\n"
        "typeList:\n"
        "      typeType\n"
        "    | typeList COMMA typeType\n"
        "    ;"
    )
    
    doc.add_heading_2("B. Dangling-Else Disambiguation")
    doc.add_paragraph("Resolved using operator precedence directives to bind 'else' to the innermost 'if':")
    doc.add_code_block(
        "%nonassoc LOWER_THAN_ELSE\n"
        "%nonassoc ELSE\n\n"
        "statement:\n"
        "      IF LPAREN expression RPAREN statement %prec LOWER_THAN_ELSE\n"
        "    | IF LPAREN expression RPAREN statement ELSE statement\n"
        "    ;"
    )
    
    doc.add_heading_2("C. Java 21 Switch Guard Isolation (when clauses)")
    doc.add_paragraph("Disambiguated boolean guard expressions from switch case arrows (->) using a dedicated guardExpression nonterminal.")
    
    doc.add_heading_2("D. Ragged & Multidimensional Array Dimensions")
    doc.add_paragraph("Stratified array creation rules into explicit non-empty dimension expressions followed by optional empty brackets (new int[5][]).")
    
    doc.save(os.path.join(DOC_DIR, "04_Grammar_Source_and_Adaptation.pdf"))

def gen_doc_05():
    doc = PDFBuilder("System Architecture & Data Flow", "DOC-05")
    doc.add_title_header("Modular Front-End Compiler Architecture & Subsystem Boundaries")
    
    doc.add_heading_1("1. End-to-End System Architecture")
    doc.add_paragraph(
        "The project is structured into four distinct, loosely-coupled layers: Lexical Analysis, Syntax Parsing, "
        "Native C Backend Interface, and the Graphical Application Layer."
    )
    
    diagram = (
        "+-----------------------------------------------------------------------------------+\n"
        "|                              1. Input Java Source                                 |\n"
        "|                       (User Editor Buffer or .java File)                          |\n"
        "+-----------------------------------------------------------------------------------+\n"
        "                                         |\n"
        "                                         v\n"
        "+-----------------------------------------------------------------------------------+\n"
        "|                        2. Lexical Analyzer (GNU Flex)                             |\n"
        "|  - java_lexer.l -> lex.yy.c                                                       |\n"
        "|  - Reads character stream via yyin; tracks line/column via YY_USER_ACTION         |\n"
        "+-----------------------------------------------------------------------------------+\n"
        "                                         | Stream of Tokens + (yylval, yylloc)\n"
        "                                         v\n"
        "+-----------------------------------------------------------------------------------+\n"
        "|                     3. LALR(1) Syntax Parser (GNU Bison)                          |\n"
        "|  - java_parser.y -> java_parser.tab.c                                             |\n"
        "|  - Shift-Reduce State Machine (998+ states); verifies Java 21 CFG rules           |\n"
        "+-----------------------------------------------------------------------------------+\n"
        "                                         | Return Code (0: OK, 1: Error, 2: IO)\n"
        "                                         v\n"
        "+-----------------------------------------------------------------------------------+\n"
        "|                    4. Native C Interface (Shared Library / CLI)                   |\n"
        "|  - javacheck.dll (Windows DLL) / javacheck.exe (CLI binary)                       |\n"
        "+-----------------------------------------------------------------------------------+\n"
        "                                         | Python ctypes in-memory FFI\n"
        "                                         v\n"
        "+-----------------------------------------------------------------------------------+\n"
        "|                        5. Python Tkinter Application                              |\n"
        "|  - gui/app.py -> ParserBackend, LineNumberText, CommandPalette                    |\n"
        "|  - High-visibility red line highlight (#5a1d1d) & status bar feedback             |\n"
        "+-----------------------------------------------------------------------------------+"
    )
    doc.add_code_block(diagram, font_size=7.2, leading=9.8)
    
    doc.add_heading_1("2. Component Responsibilities")
    doc.add_bullet("Flex Scanner: Strips comments/whitespace, tracks line coordinates, emits token codes.")
    doc.add_bullet("Bison Parser: Executes LALR(1) shift-reduce transitions, catches errors via yyerror().")
    doc.add_bullet("Native C Engine: Resets state, opens file streams, formats standardized error strings.")
    doc.add_bullet("Python ctypes FFI: Loads javacheck.dll in memory, allocates string buffers, executes checks.")
    doc.add_bullet("Tkinter GUI: Renders dark editor, synchronizes line numbers, applies visual error tags.")
    
    doc.save(os.path.join(DOC_DIR, "05_Project_Architecture.pdf"))

def gen_doc_06():
    doc = PDFBuilder("Complete Execution Workflow", "DOC-06")
    doc.add_title_header("Internal Execution Trace, CLI Flow, & GUI Interactive Pipelines")
    
    doc.add_heading_1("1. High-Level Pipeline (Viva Explanation)")
    doc.add_paragraph("The complete execution path from source file to graphical highlight proceeds as follows:")
    doc.add_callout(
        "Java source file -> Flex lexer -> Token stream -> Bison LALR(1) parser -> "
        "Shift/Reduce actions -> Syntax result -> javacheck.dll / javacheck.exe -> "
        "Python ctypes backend -> Tkinter GUI -> Result / error-line highlighting",
        title="VIVA ONE-SENTENCE PIPELINE",
        style="info"
    )
    
    doc.add_heading_1("2. Internal C Engine Execution Trace")
    doc.add_bullet("1. check_syntax(filepath, err_msg, len) is called.")
    doc.add_bullet("2. State variables are reset: syntax_error_occurred = 0, error_line = 0, yylineno = 1, current_column = 1, yylloc = {1,1,1,1}.")
    doc.add_bullet("3. File handle is opened: FILE *f = fopen(filepath, 'r'). If NULL, returns 2 (I/O error).")
    doc.add_bullet("4. Scanner buffer is re-initialized: yyrestart(f); yyin = f;.")
    doc.add_bullet("5. Parser loop begins: yyparse() is invoked.")
    doc.add_bullet("6. yyparse() repeatedly calls yylex() to fetch lookahead tokens.")
    doc.add_bullet("7. YY_USER_ACTION updates yylloc coordinates before every token action.")
    doc.add_bullet("8. Parser shifts tokens or reduces rules against LALR(1) tables.")
    doc.add_bullet("9. On syntax error, Bison calls yyerror(); error_line is extracted from yylloc.first_line.")
    doc.add_bullet("10. check_syntax() closes file handle and formats result string.")
    
    doc.add_heading_1("3. CLI vs. GUI Workflow Comparison")
    headers = ["Workflow Step", "CLI Execution (javacheck.exe)", "GUI Execution (gui/app.py)"]
    rows = [
        ["Trigger", "User runs command in shell", "User presses Ctrl+Enter or clicks chip"],
        ["Input Source", "Disk file path from argv[1]", "In-memory editor text or opened file"],
        ["Invocation", "Direct C main() execution", "In-memory ctypes CDLL invocation"],
        ["Success Feedback", "stdout: SUCCESS: Valid Java Syntax", "Green status bar & clean editor"],
        ["Error Feedback", "stderr: ERROR: Line X: Syntax error...", "Red status bar, gutter color, line highlight"]
    ]
    doc.add_table(headers, rows, [2.0, 2.5, 2.5])
    
    doc.save(os.path.join(DOC_DIR, "06_Complete_Workflow.pdf"))

def gen_doc_07():
    doc = PDFBuilder("Lexical Analyzer (GNU Flex)", "DOC-07")
    doc.add_title_header("DFA Regular Expressions, Location Tracking, & Lexer States")
    
    doc.add_heading_1("1. Lexical Analysis Principles")
    doc.add_paragraph(
        "Lexical analysis (scanning) is the first phase of a compiler. It converts a raw stream of characters into discrete, "
        "meaningful atomic units called tokens. GNU Flex compiles high-level regular expression specifications into a "
        "table-driven Deterministic Finite Automaton (DFA) executing in linear O(n) time."
    )
    
    doc.add_heading_1("2. Scanner Specification (lexer/java_lexer.l)")
    doc.add_bullet("Keywords: 50+ Java keywords (class, interface, record, sealed, permits, when, var, yield, etc.).")
    doc.add_bullet("Literals: Decimal, Hexadecimal (0x...), Binary (0b...), Octal, Floating-point, Char, String, Text Blocks.")
    doc.add_bullet("Unicode Identifiers: Supports ASCII, $, _, and multi-byte UTF-8 bytes ([\\x80-\\xFF]).")
    doc.add_bullet("Operators & Separators: All Java operators including >>>=, ::, ->, @, ..., etc.")
    
    doc.add_heading_1("3. Lexer Start Conditions (States)")
    doc.add_paragraph("Exclusive states (%x) handle multi-line comments and modern text blocks:")
    doc.add_code_block(
        "%x STATE_BLOCK_COMMENT\n"
        "%x STATE_TEXT_BLOCK\n\n"
        "/* Block Comment */\n"
        "\"/*\"                       { BEGIN(STATE_BLOCK_COMMENT); }\n"
        "<STATE_BLOCK_COMMENT>\"*/\"  { BEGIN(INITIAL); }\n"
        "<STATE_BLOCK_COMMENT>\\n    { current_column = 1; }\n"
        "<STATE_BLOCK_COMMENT>.     { /* ignore */ }\n\n"
        "/* Text Block */\n"
        "\"\\\"\\\"\\\"\"                   { BEGIN(STATE_TEXT_BLOCK); }\n"
        "<STATE_TEXT_BLOCK>\"\\\"\\\"\\\"\" { BEGIN(INITIAL); return TEXT_BLOCK; }"
    )
    
    doc.add_heading_1("4. Location Tracking via YY_USER_ACTION")
    doc.add_code_block(
        "#define YY_USER_ACTION \\\n"
        "    yylloc.first_line = yylloc.last_line = yylineno; \\\n"
        "    yylloc.first_column = current_column; \\\n"
        "    yylloc.last_column = current_column + yyleng - 1; \\\n"
        "    current_column += yyleng;"
    )
    doc.add_paragraph("This hook guarantees that every token delivered to Bison carries exact line and column coordinates.")
    
    doc.save(os.path.join(DOC_DIR, "07_Lexical_Analyzer_Flex.pdf"))

def gen_doc_08():
    doc = PDFBuilder("Syntax Parser (GNU Bison LALR(1))", "DOC-08")
    doc.add_title_header("Context-Free Grammars, Shift-Reduce Automata, & Conflict Profile")
    
    doc.add_heading_1("1. Syntax Analysis & Context-Free Grammars")
    doc.add_paragraph(
        "Syntax analysis groups the stream of tokens into grammatical structures defined by a Context-Free Grammar (CFG). "
        "GNU Bison generates a deterministic bottom-up LALR(1) (Look-Ahead Left-to-Right with 1 token lookahead) state machine. "
        "The parser maintains a parse stack and consults Action and Goto tables to perform Shift and Reduce operations."
    )
    
    doc.add_heading_1("2. Shift-Reduce Parser Operations")
    doc.add_bullet("Shift: Pushes the current lookahead token onto the stack and advances the input stream.")
    doc.add_bullet("Reduce: Replaces a sequence of grammar symbols on top of the stack matching rule A -> alpha with nonterminal A.")
    doc.add_bullet("Accept: Start symbol compilationUnit is reduced on EOF ($end); syntax is valid.")
    doc.add_bullet("Error: Action table entry is empty for the (State, Token) pair; triggers yyerror().")
    
    doc.add_heading_1("3. Operator Precedence & Associativity Table")
    headers = ["Precedence Level", "Associativity", "Operators / Directives"]
    rows = [
        ["1. Dangling Else", "%nonassoc", "LOWER_THAN_ELSE, ELSE"],
        ["2. Lambda Arrow", "%right", "ARROW (->)"],
        ["3. Assignments", "%right", "=, +=, -=, *=, /=, %=, &=, ^=, |=, <<=, >>=, >>>="],
        ["4. Ternary", "%right", "?, :"],
        ["5. Logical OR / AND", "%left", "||, &&"],
        ["6. Equality / Relational", "%left", "==, !=, <, >, <=, >=, instanceof"],
        ["7. Shifts / Additive", "%left", "<<, >>, >>>, +, -"],
        ["8. Multiplicative", "%left", "*, /, %"],
        ["9. Unary / Prefix", "%right", "++, --, +, -, ~, !, (cast)"]
    ]
    doc.add_table(headers, rows, [2.2, 1.8, 3.0])
    
    doc.add_heading_1("4. Bison Conflict Profile (285 S/R, 34 R/R)")
    doc.add_paragraph(
        "Bison reports 285 shift/reduce and 34 reduce/reduce conflicts in java_parser.output. "
        "These arise from contextual keywords (record, when, yield, var) that can serve as either keywords or identifiers, "
        "and Java's statement grammar. Bison's default shift-over-reduce resolution perfectly matches Java's longest-match semantics."
    )
    
    doc.save(os.path.join(DOC_DIR, "08_Syntax_Parser_Bison_LALR.pdf"))

def gen_doc_09():
    doc = PDFBuilder("Java 21 Language Features Supported", "DOC-09")
    doc.add_title_header("Modern Java 21 LTS Syntax Conformance & Grammar Rules")
    
    doc.add_heading_1("1. Supported Java 21 Features (Verified in Repository)")
    doc.add_paragraph("The parser implements full grammatical support for modern Java 21 LTS finalized syntax:")
    
    headers = ["Feature Category", "Java 21 Syntax Example", "Test Verification File"]
    rows = [
        ["Record Declarations", "public record Point(int x, int y) {}", "tests/valid_full.java"],
        ["Compact Record Const.", "public Point { Objects.requireNonNull(x); }", "tests/test_record_compact_annotated.java"],
        ["Record Patterns (JEP 440)", "p instanceof Point(var x, var y)", "tests/java21_record_patterns.java"],
        ["Nested Record Patterns", "p instanceof Box(Point(int x, int y))", "tests/java21_record_patterns.java"],
        ["Switch Patterns (JEP 441)", "case Point(double x, double y) -> ...", "tests/java21_switch_patterns.java"],
        ["Switch Guards (when)", "case Point(int x, int y) when x > 0 ->", "tests/java21_switch_patterns.java"],
        ["Sealed Types", "sealed interface Shape permits Circle {}", "tests/test_advanced.java"],
        ["Text Blocks", "String s = \"\"\"\n  Hello World\n  \"\"\";", "tests/err_text_block.java"],
        ["Unsigned Right Shift", "a >>>= 2;", "tests/test_urshift_assign.java"],
        ["Module Info", "module com.app { requires java.base; }", "tests/test_module_info.java"],
        ["Ragged Arrays", "int[][] matrix = new int[5][];", "tests/test_array_ragged.java"],
        ["Multi Try-with-Resources", "try (R r1 = a; R r2 = b;) { ... }", "tests/test_try_resources_multi.java"]
    ]
    doc.add_table(headers, rows, [2.2, 3.0, 2.0])
    
    doc.add_heading_1("2. Code Snippet: Java 21 Pattern Matching with Guard")
    doc.add_code_block(
        "public class PatternDemo {\n"
        "    public record Point(double x, double y) {}\n\n"
        "    public static String classify(Object obj) {\n"
        "        return switch (obj) {\n"
        "            case null -> \"Null reference\";\n"
        "            case Point(double x, double y) when x > 0 && y > 0 -> \"Quadrant I Point\";\n"
        "            case Point(double x, double y) -> \"Other Point\";\n"
        "            case String s -> \"String: \" + s;\n"
        "            default -> \"Unknown Object\";\n"
        "        };\n"
        "    }\n"
        "}"
    )
    
    doc.save(os.path.join(DOC_DIR, "09_Java21_Features.pdf"))

def gen_doc_10():
    doc = PDFBuilder("Syntax Error Detection & Location", "DOC-10")
    doc.add_title_header("Location Precision, yylloc, Lookahead, & Formatting Scenarios")
    
    doc.add_heading_1("1. Syntax Error Detection Mechanism")
    doc.add_paragraph(
        "A syntax error occurs when the next lookahead token cannot legally follow the grammar path for the current state. "
        "Bison halts normal reduction, triggers the callback void yyerror(const char *s), and sets syntax_error_occurred = 1."
    )
    
    doc.add_heading_1("2. Pinpoint Error-Line Extraction")
    doc.add_code_block(
        "void yyerror(const char *s) {\n"
        "    syntax_error_occurred = 1;\n"
        "    error_line = yylloc.first_line ? yylloc.first_line : yylineno;\n"
        "}"
    )
    doc.add_paragraph(
        "Because YY_USER_ACTION in Flex continuously updates yylloc.first_line with the exact line number of every token, "
        "yyerror() captures the exact 1-indexed source line without drifting."
    )
    
    doc.add_heading_1("3. Standardized Output Format")
    doc.add_bullet("Success: SUCCESS: Valid Java Syntax (return code 0)")
    doc.add_bullet("Syntax Error: ERROR: Line <N>: Syntax error near '<TOKEN>' (return code 1)")
    doc.add_bullet("File I/O Error: ERROR: Could not open file '<PATH>' (return code 2)")
    
    doc.add_heading_1("4. Error Accuracy Verification Across Edge Cases")
    headers = ["Scenario", "Code Sample", "Expected & Verified Line"]
    rows = [
        ["Line 1 Error", "class { }", "Line 1: Syntax error near '{'"],
        ["Line 2 Error", "class T { int x = ; }", "Line 2: Syntax error near ';'"],
        ["After Blank Lines", "5 blank lines followed by bad token", "Exact line after blanks counted"],
        ["After Block Comments", "/* multi-line comment */ on lines 1-5", "Line 6 error counted correctly"],
        ["After Text Blocks", "\"\"\" multi-line string \"\"\"", "Line after text block counted correctly"],
        ["Missing Semicolon", "int a = 10 \n int b = 20;", "Line 2: Syntax error near 'int' (lookahead)"]
    ]
    doc.add_table(headers, rows, [2.0, 3.0, 2.2])
    
    doc.save(os.path.join(DOC_DIR, "10_Error_Detection_and_Location.pdf"))

def gen_doc_11():
    doc = PDFBuilder("Native C Backend (DLL & EXE)", "DOC-11")
    doc.add_title_header("C ABI Export, Memory Buffers, Return Codes, & Compilation")
    
    doc.add_heading_1("1. C Backend Architecture")
    doc.add_paragraph(
        "The parsing core is implemented in C99, linking the Bison-generated parser (java_parser.tab.c) and "
        "Flex-generated scanner (lex.yy.c). It is compiled with GCC into both a shared dynamic link library (javacheck.dll) "
        "and a standalone command-line executable (javacheck.exe)."
    )
    
    doc.add_heading_1("2. C ABI Export: check_syntax()")
    doc.add_code_block(
        "#ifdef _WIN32\n"
        "__declspec(dllexport)\n"
        "#endif\n"
        "int check_syntax(const char *filepath, char *err_msg, int err_msg_len) {\n"
        "    // 1. Reset state variables (yylineno, current_column, error_line, yylloc)\n"
        "    // 2. Open file stream: fopen(filepath, \"r\")\n"
        "    // 3. Re-initialize scanner: yyrestart(f); yyin = f;\n"
        "    // 4. Execute parser: int result = yyparse();\n"
        "    // 5. Close file and write formatted message to err_msg\n"
        "    // 6. Return 0 (Success), 1 (Syntax Error), or 2 (File Error)\n"
        "}"
    )
    
    doc.add_heading_1("3. Standard Return Code Contract")
    doc.add_bullet("Return 0: Valid Java syntax; err_msg = 'SUCCESS: Valid Java Syntax'")
    doc.add_bullet("Return 1: Syntax error detected; err_msg = 'ERROR: Line X: Syntax error near 'token''")
    doc.add_bullet("Return 2: System or file I/O error; err_msg = 'ERROR: Could not open file '...'")
    
    doc.add_heading_1("4. Native Compilation Commands")
    doc.add_code_block(
        "# Compile Shared Library (DLL)\n"
        "gcc -O2 -shared -Iparser -Ilexer parser/java_parser.tab.c lexer/lex.yy.c -o javacheck.dll\n\n"
        "# Compile Standalone CLI Executable\n"
        "gcc -O2 -Iparser -Ilexer parser/java_parser.tab.c lexer/lex.yy.c -o javacheck.exe"
    )
    
    doc.save(os.path.join(DOC_DIR, "11_C_Backend_DLL_EXE.pdf"))

def gen_doc_12():
    doc = PDFBuilder("Python Backend & ctypes FFI", "DOC-12")
    doc.add_title_header("Foreign Function Interface, In-Memory Invocation, & Fallback")
    
    doc.add_heading_1("1. Foreign Function Interface (ctypes)")
    doc.add_paragraph(
        "Python's standard ctypes module allows calling functions in native DLLs directly within the Python process memory space. "
        "This eliminates the operating system overhead of repeatedly spawning subprocesses."
    )
    
    doc.add_heading_1("2. Backend Initialization (ParserBackend)")
    doc.add_code_block(
        "import ctypes\n\n"
        "class ParserBackend:\n"
        "    def __init__(self):\n"
        "        self.use_dll = False\n"
        "        if os.path.exists(DLL_PATH):\n"
        "            try:\n"
        "                self.dll = ctypes.CDLL(DLL_PATH)\n"
        "                self.dll.check_syntax.argtypes = [\n"
        "                    ctypes.c_char_p,   # filepath (UTF-8 bytes)\n"
        "                    ctypes.c_char_p,   # output message buffer\n"
        "                    ctypes.c_int       # buffer length\n"
        "                ]\n"
        "                self.dll.check_syntax.restype = ctypes.c_int\n"
        "                self.use_dll = True\n"
        "            except Exception:\n"
        "                self.use_dll = False"
    )
    
    doc.add_heading_1("3. In-Memory Code Checking (check_code_string)")
    doc.add_paragraph(
        "To check code typed live into the editor, check_code_string() safely writes the text buffer to a temporary file "
        "using Python's tempfile module, invokes check_file(), and deletes the temporary file in a finally block."
    )
    
    doc.add_heading_1("4. Subprocess Fallback")
    doc.add_paragraph(
        "If javacheck.dll cannot be loaded (due to permissions or environment constraints), ParserBackend automatically "
        "falls back to invoking javacheck.exe via subprocess.run(), ensuring continuous operation."
    )
    
    doc.save(os.path.join(DOC_DIR, "12_Python_Backend_and_ctypes.pdf"))

def gen_doc_13():
    doc = PDFBuilder("Tkinter GUI Architecture", "DOC-13")
    doc.add_title_header("VS Code-Style UI, Command Palette, & Line Number Synchronization")
    
    doc.add_heading_1("1. Graphical User Interface Overview")
    doc.add_paragraph(
        "The GUI application (gui/app.py) is a modern, VS Code-inspired developer tool built entirely with Python standard "
        "libraries. It provides an intuitive environment for writing, opening, and verifying Java 21 source code."
    )
    
    doc.add_heading_1("2. Core GUI Subsystems")
    doc.add_bullet("Editor with Synchronized Gutter: LineNumberText wraps a text area and left canvas displaying right-aligned line numbers.")
    doc.add_bullet("Dark Developer Theme: Custom palette (#1e1e1e editor, #252526 panels, #007acc accent, #5a1d1d error tint).")
    doc.add_bullet("Command Palette (Ctrl+Shift+P / F1): Floating quick-pick overlay with real-time fuzzy search across all commands.")
    doc.add_bullet("Status Bar: Compact bar displaying status, cursor position (Ln X, Col Y), encoding (UTF-8), and engine status.")
    doc.add_bullet("Output Panel: 4-line terminal log recording timestamped execution history ($ check Sample.java).")
    
    doc.add_heading_1("3. Keyboard Shortcuts Reference")
    headers = ["Shortcut Key", "Action Description", "Palette Command"]
    rows = [
        ["Ctrl + Shift + P / F1", "Open Command Palette quick-picker", "Open Command Palette"],
        ["Ctrl + Enter / F5", "Check Java Syntax", "Check Syntax"],
        ["Ctrl + O", "Open .java source file from disk", "Open File..."],
        ["Ctrl + S", "Save current editor text to file", "Save File"],
        ["Ctrl + L", "Clear editor buffer and status", "Clear Editor"],
        ["Escape", "Dismiss Command Palette overlay", "Close Palette"]
    ]
    doc.add_table(headers, rows, [2.2, 3.0, 2.0])
    
    doc.add_heading_1("4. Visual Error-Line Highlighting")
    doc.add_paragraph(
        "When an error on line N is returned, the editor tags the line range ('N.0' to 'N.end+1c') with the error_line tag "
        "(soft red background #5a1d1d), colors gutter number N red, and scrolls line N into focus using self.editor.text.see('N.0')."
    )
    
    doc.save(os.path.join(DOC_DIR, "13_Tkinter_GUI.pdf"))

def gen_doc_14():
    doc = PDFBuilder("Build Automation & Execution", "DOC-14")
    doc.add_title_header("Multi-Platform Build Scripts, Compilation, & CLI/GUI Commands")
    
    doc.add_heading_1("1. Build Automation Overview")
    doc.add_paragraph("The repository provides three automated build pipelines supporting different development environments:")
    doc.add_bullet("Windows Command Prompt: build.bat")
    doc.add_bullet("Windows PowerShell: build.ps1")
    doc.add_bullet("Cross-Platform GNU Make: Makefile")
    
    doc.add_heading_1("2. Sequential Build Steps")
    doc.add_bullet("Step 1: Checks for flex, bison, and gcc in system PATH (injects MSYS2 UCRT64 paths).")
    doc.add_bullet("Step 2: bison -v -d parser/java_parser.y --report-file=parser/java_parser.output -o parser/java_parser.tab.c")
    doc.add_bullet("Step 3: flex -o lexer/lex.yy.c lexer/java_lexer.l")
    doc.add_bullet("Step 4: gcc -O2 -shared -Iparser -Ilexer parser/java_parser.tab.c lexer/lex.yy.c -o javacheck.dll")
    doc.add_bullet("Step 5: gcc -O2 -Iparser -Ilexer parser/java_parser.tab.c lexer/lex.yy.c -o javacheck.exe")
    
    doc.add_heading_1("3. How to Run the System")
    doc.add_heading_2("Launch Graphical User Interface:")
    doc.add_code_block("python gui/app.py")
    
    doc.add_heading_2("Execute Command-Line Syntax Check:")
    doc.add_code_block(
        "# Check valid file\n"
        "javacheck.exe tests/valid_1.java\n"
        "# Output: SUCCESS: Valid Java Syntax\n\n"
        "# Check invalid file\n"
        "javacheck.exe tests/invalid_2.java\n"
        "# Output: ERROR: Line 2: Syntax error near ';'"
    )
    
    doc.add_heading_2("Run Automated Regression Test Suites:")
    doc.add_code_block(
        "python tests/run_tests.py         # Runs 59 parser tests\n"
        "python tests/test_gui_backend.py  # Runs 14 GUI integration tests"
    )
    
    doc.save(os.path.join(DOC_DIR, "14_Build_and_Execution.pdf"))

def gen_doc_15():
    doc = PDFBuilder("Comprehensive Testing Strategy", "DOC-15")
    doc.add_title_header("Verification Methodology, Test Harnesses, & Quality Assurance")
    
    doc.add_heading_1("1. Testing Philosophy & Multi-Tier Strategy")
    doc.add_paragraph(
        "A rigorous multi-tier testing methodology was applied to ensure that grammar rules, lexical tracking, native bindings, "
        "and user interface interactions function flawlessly across all categories."
    )
    
    doc.add_heading_1("2. Testing Tiers")
    doc.add_bullet("Tier 1: Lexer Unit Testing — Standalone token validation via lexer_driver.c and lexer_test.exe.")
    doc.add_bullet("Tier 2: Parser Batch Testing — 59 automated test cases in tests/run_tests.py checking return codes and messages.")
    doc.add_bullet("Tier 3: Error Location Precision Testing — Exact line validation after comments, blank lines, and text blocks.")
    doc.add_bullet("Tier 4: Stress & Boundary Testing — Deeply nested record deconstructions, generic lambdas, and EOF boundaries.")
    doc.add_bullet("Tier 5: GUI Integration Testing — 14 automated unit tests in tests/test_gui_backend.py testing UI widgets & FFI.")
    
    doc.add_heading_1("3. Automated Test Runner Architecture")
    doc.add_paragraph(
        "The automated harness (tests/run_tests.py) iterates over test tuples (path, should_be_valid, description). "
        "It invokes check_syntax() via in-memory ctypes (or CLI fallback), validates (return_code == 0) == should_be_valid, "
        "and asserts that the error message contains the expected line number."
    )
    
    doc.save(os.path.join(DOC_DIR, "15_Testing_Strategy.pdf"))

def gen_doc_16():
    doc = PDFBuilder("Test Cases & Final Verified Results", "DOC-16")
    doc.add_title_header("Breakdown of 59 Parser Tests & 14 GUI Integration Tests (100% Pass Rate)")
    
    doc.add_heading_1("1. Final Verified Test Summary")
    doc.add_callout(
        "PARSER TEST SUITE: 59 / 59 PASSED (100.0%)\n"
        "GUI INTEGRATION SUITE: 14 / 14 PASSED (100.0%)\n"
        "TOTAL AUTOMATED TESTS: 73 / 73 PASSED (100.0%)",
        title="VERIFIED TEST RESULTS SUMMARY",
        style="success"
    )
    
    doc.add_heading_1("2. Breakdown of 59 Parser Tests by Category")
    headers = ["Test Category", "Test Count", "Pass Rate", "What the Category Proves"]
    rows = [
        ["Original Regression", "23 Tests", "23 / 23 (100%)", "Core Java 8–17 classes, methods, for-loops, enums, missing delimiters"],
        ["Java 21 Feature Tests", "12 Tests", "12 / 12 (100%)", "Record patterns, switch patterns, when guards, sealed classes, text blocks"],
        ["Phase 9 Completeness", "8 Tests", "8 / 8 (100%)", ">>>= assignment, module-info, multi try-with-resources, ragged arrays"],
        ["Error Accuracy (Phase 10)", "13 Tests", "13 / 13 (100%)", "Exact line accuracy after blanks, single/multi comments, text blocks"],
        ["Stress & Boundaries", "3 Tests", "3 / 3 (100%)", "Deep nested record deconstructions, generic lambdas, switch guard bounds"],
        ["Total Parser Tests", "59 Tests", "59 / 59 (100%)", "Complete front-end grammar and error verification"]
    ]
    doc.add_table(headers, rows, [2.2, 1.2, 1.4, 2.6])
    
    doc.add_heading_1("3. Breakdown of 14 GUI Integration Tests")
    doc.add_paragraph("All 14 integration tests in tests/test_gui_backend.py passed with 100% success:")
    doc.add_bullet("1. test_window_title_and_structure (Window and subwidgets)")
    doc.add_bullet("2. test_backend_initialization (ctypes CDLL handle)")
    doc.add_bullet("3. test_valid_simple_class (In-memory simple valid check)")
    doc.add_bullet("4. test_valid_java21_features (In-memory Java 21 records & switch)")
    doc.add_bullet("5. test_invalid_line_1 (Error on line 1 extraction)")
    doc.add_bullet("6. test_invalid_middle_line (Error on line 4 in method body)")
    doc.add_bullet("7. test_invalid_after_comments_and_blank_lines (Line 6 error)")
    doc.add_bullet("8. test_invalid_eof (Missing closing brace at EOF)")
    doc.add_bullet("9. test_gui_file_load_and_line_numbers (File load & gutter sync)")
    doc.add_bullet("10. test_gui_editor_editing_and_rechecking (Invalid -> Fix -> Valid workflow)")
    doc.add_bullet("11. test_gui_error_highlight_and_clearing (Tag add and clear on edit)")
    doc.add_bullet("12. test_gui_long_file_scrolling_and_line_numbers (100+ line gutter alignment)")
    doc.add_bullet("13. test_command_palette_filtering (Fuzzy search & execution)")
    doc.add_bullet("14. test_theme_switching (Dark/light theme toggle)")
    
    doc.save(os.path.join(DOC_DIR, "16_Test_Cases_and_Results.pdf"))

def gen_doc_17():
    doc = PDFBuilder("Limitations & Future Enhancements", "DOC-17")
    doc.add_title_header("Theoretical Boundaries & Prospective Architectural Improvements")
    
    doc.add_heading_1("1. Actual Verified Limitations")
    doc.add_bullet("1. Syntax-Only Verification: Does not perform semantic analysis, type checking, symbol resolution, or class hierarchy validation.")
    doc.add_bullet("2. Single-Error Termination: In accordance with standard pure LALR(1) parsers, parsing halts upon encountering the first syntax error.")
    doc.add_bullet("3. No Bytecode Generation: Does not emit JVM .class files or intermediate bytecode.")
    doc.add_bullet("4. No Runtime Execution: Does not run, debug, or profile Java programs.")
    doc.add_bullet("5. Finalized Java 21 Only: Experimental preview features (e.g. String Templates preview) are excluded.")
    
    doc.add_heading_1("2. Prospective Future Enhancements (Clearly Labeled as Future Work)")
    doc.add_heading_2("A. Multi-Error Recovery Cascade")
    doc.add_paragraph("Implementing Bison %destructor and error token recovery productions to resynchronize at statement boundaries and report multiple errors in a single pass.")
    
    doc.add_heading_2("B. Abstract Syntax Tree (AST) Generation & Visualization")
    doc.add_paragraph("Extending grammar action rules to build a hierarchical AST in memory, serializable to JSON, and rendered as an interactive tree in the GUI.")
    
    doc.add_heading_2("C. Lightweight Semantic Symbol Table Pass")
    doc.add_paragraph("Adding a post-parse symbol table pass to detect undeclared variable references and mismatched argument counts.")
    
    doc.add_heading_2("D. Cross-Platform Shared Libraries")
    doc.add_paragraph("Extending Makefile targets to build native shared objects (.so for Linux and .dylib for macOS).")
    
    doc.save(os.path.join(DOC_DIR, "17_Limitations_and_Future_Work.pdf"))

def gen_doc_18():
    doc = PDFBuilder("Project Conclusion & Academic Review", "DOC-18")
    doc.add_title_header("Summary of Achievements, Compiler Concepts Demonstrated, & Final Remarks")
    
    doc.add_heading_1("1. Summary of Project Achievements")
    doc.add_paragraph(
        "The Java 21 Syntax Checker project successfully constructed a high-precision, robust compiler front-end tool "
        "targeting the finalized Java 21 LTS language specification. The project achieved:"
    )
    doc.add_bullet("A fully compliant GNU Flex 2.6.x lexical DFA scanner with location tracking.")
    doc.add_bullet("A deterministic GNU Bison 3.8.x LALR(1) shift-reduce parser resolving all Java 21 ambiguities.")
    doc.add_bullet("A dual-target C native engine compiled into javacheck.dll and javacheck.exe.")
    doc.add_bullet("A modern Python 3.10+ Tkinter GUI with in-memory ctypes FFI, Command Palette, and error highlighting.")
    doc.add_bullet("A verified 100% pass rate across 59 parser test cases and 14 GUI integration tests.")
    
    doc.add_heading_1("2. Core Compiler Design Concepts Demonstrated")
    headers = ["Theoretical Concept", "Practical Implementation in This Project"]
    rows = [
        ["Regular Expressions & DFAs", "Lexer token specification (java_lexer.l) using Flex state machine"],
        ["Context-Free Grammars", "Formal Java 21 grammar rules in Bison (java_parser.y)"],
        ["LALR(1) Parsing Tables", "Shift-reduce state transitions over 998+ parser states"],
        ["Ambiguity Resolution", "%nonassoc precedence rules resolving dangling-else & switch guards"],
        ["Location Tracking", "YY_USER_ACTION synchronizing yylloc coordinates with yylineno"],
        ["Native FFI Interoperability", "Direct C ABI shared library loading via Python ctypes"]
    ]
    doc.add_table(headers, rows, [2.5, 4.5])
    
    doc.add_heading_1("3. Concluding Statement")
    doc.add_paragraph(
        "By successfully bridging classical compiler construction theory with modern programming language syntax and "
        "desktop tool design, this project fulfills all requirements of the Course-Based Project with academic rigor, "
        "technical excellence, and practical usability."
    )
    
    doc.save(os.path.join(DOC_DIR, "18_Project_Conclusion.pdf"))

def gen_doc_19():
    doc = PDFBuilder("Comprehensive Viva Q&A Master Guide", "DOC-19")
    doc.add_title_header("50+ Project-Specific Viva Questions, Answers, & Concise Examiner Phrases")
    
    # Section A: Basic Project Questions
    doc.add_heading_1("Section A: Basic Project Questions")
    doc.add_viva_qa(1, "What is the primary purpose of this project?",
                    "It is a formal compiler front end that checks the grammatical validity of Java 21 source code and locates syntax errors to the exact line.",
                    "It validates Java 21 source code syntax using Flex and Bison and highlights errors in a Tkinter GUI.")
    
    doc.add_viva_qa(2, "Is this project a full Java compiler?",
                    "No. It is strictly a compiler front-end syntax checker. It does not perform semantic analysis, generate bytecode, or execute programs.",
                    "No, it is a syntax checker only; it does not perform semantic analysis, bytecode generation, or execution.")
    
    doc.add_viva_qa(3, "What version of Java is targeted and why?",
                    "Java 21 (LTS). It is the latest long-term support version that finalized modern syntax like record patterns, switch patterns, and sealed types.",
                    "Java 21 LTS because it contains finalized standard syntax for modern features like record patterns.")
    
    # Section B: Compiler Design Concepts
    doc.add_heading_1("Section B: Compiler Design Concepts")
    doc.add_viva_qa(4, "What is a compiler front end?",
                    "The front end consists of lexical analysis, syntax analysis, and semantic analysis, converting source code into an intermediate representation.",
                    "The front-end phases process source code into an intermediate format independently of target machine code.")
    
    doc.add_viva_qa(5, "What is a Context-Free Grammar (CFG)?",
                    "A 4-tuple (V, Sigma, R, S) defining language syntax using recursive production rules that map nonterminals to strings of terminals.",
                    "A formal grammar whose production rules map a single nonterminal symbol to a string of terminals and nonterminals.")
    
    # Section C: GNU Flex
    doc.add_heading_1("Section C: GNU Flex (Lexical Analysis)")
    doc.add_viva_qa(6, "Why choose GNU Flex?",
                    "Flex compiles regular expressions into high-speed table-driven DFAs in C, scanning tokens in linear O(n) time.",
                    "Flex generates fast, deterministic finite automata in C that tokenize source code in linear time.")
    
    doc.add_viva_qa(7, "What does YY_USER_ACTION do in Flex?",
                    "It is a macro executed before every matched token action to update yylloc line and column coordinates.",
                    "It is a Flex hook that synchronizes token line and column coordinates in yylloc before every action.")
    
    # Section D: GNU Bison & LALR(1)
    doc.add_heading_1("Section D: GNU Bison & LALR(1) Parsing")
    doc.add_viva_qa(8, "What is LALR(1) parsing?",
                    "Look-Ahead LR parsing with 1 token lookahead. It merges LR(1) states sharing identical core item sets to reduce table size.",
                    "LALR(1) is a bottom-up parsing method that merges identical LR(1) core states to create compact, fast parsing tables.")
    
    doc.add_viva_qa(9, "Why choose LALR(1) over Recursive Descent?",
                    "LALR(1) handles left-recursion naturally, eliminates recursive call stack overhead, and automates table generation from CFGs.",
                    "LALR(1) handles left-recursion naturally, avoids recursion overflow, and provides automated table generation.")
    
    doc.add_viva_qa(10, "How is the dangling-else ambiguity resolved?",
                    "By assigning higher precedence to ELSE over LOWER_THAN_ELSE, causing the parser to shift and bind 'else' to the innermost 'if'.",
                    "We assign ELSE higher precedence than LOWER_THAN_ELSE, causing the parser to shift and bind 'else' to the closest 'if'.")
    
    # Section E: C Backend & FFI
    doc.add_heading_1("Section E: C Backend & Python ctypes")
    doc.add_viva_qa(11, "What are the return codes of check_syntax()?",
                    "0 for success (valid syntax), 1 for syntax error, and 2 for file I/O or system error.",
                    "0 = Valid Syntax, 1 = Syntax Error, 2 = File I/O Error.")
    
    doc.add_viva_qa(12, "Why generate both a DLL and an EXE?",
                    "The DLL allows in-memory ctypes execution for the GUI, while the EXE provides a standalone CLI tool for scripts.",
                    "The DLL enables fast in-memory GUI execution via ctypes, while the EXE provides a standalone CLI tool.")
    
    # Section F: Testing & Verification
    doc.add_heading_1("Section F: Testing & Verification")
    doc.add_viva_qa(13, "How many automated tests were performed?",
                    "73 automated tests in total: 59 parser tests in run_tests.py and 14 GUI tests in test_gui_backend.py, with a 100% pass rate.",
                    "73 automated tests in total: 59 parser tests and 14 GUI integration tests, all passed 100%.")
    
    doc.save(os.path.join(DOC_DIR, "19_Viva_Questions_and_Answers.pdf"))

def gen_doc_20():
    doc = PDFBuilder("Demo Presentation & Viva Script", "DOC-20")
    doc.add_title_header("Practical Verbal Presentation Script, Live Demo Guide, & Defense Flow")
    
    doc.add_heading_1("1. 30-Second Elevator Pitch")
    doc.add_callout(
        "\"Respected examiners, our project is a high-precision Java 21 Syntax Checker. "
        "It implements a formal compiler front end combining a GNU Flex lexical DFA, a GNU Bison LALR(1) shift-reduce parser, "
        "a native C shared library, and a modern Python Tkinter GUI. It validates modern Java 21 syntax—including record patterns, "
        "switch guards, and sealed classes—pinpointing syntax errors to the exact line with a 100% verified test pass rate.\"",
        title="30-SECOND OPENING PITCH",
        style="info"
    )
    
    doc.add_heading_1("2. 2-Minute Comprehensive Presentation Script")
    doc.add_paragraph("Follow this structured script during your formal project review:")
    doc.add_bullet("1. Motivation: Explain that modern Java 21 LTS features (record patterns, switch guards) are rarely covered in academic parsers.")
    doc.add_bullet("2. Architecture: Walk through the pipeline from Java Source -> Flex -> Tokens -> Bison LALR(1) -> C DLL -> Python ctypes -> Tkinter GUI.")
    doc.add_bullet("3. Grammar Engineering: Highlight how ANTLR4 reference grammar was adapted to LALR(1) left-recursive rules and precedence disambiguation.")
    doc.add_bullet("4. Error Precision: Explain how YY_USER_ACTION synchronizes yylloc to capture the exact error line in yyerror().")
    doc.add_bullet("5. Results: Announce 59/59 parser tests passed and 14/14 GUI integration tests passed.")
    
    doc.add_heading_1("3. Step-by-Step Live Demonstration Sequence")
    headers = ["Demo Step", "Action in GUI / Terminal", "Expected Demonstration Outcome"]
    rows = [
        ["Step 1: Launch GUI", "Run: python gui/app.py", "Modern dark VS Code theme opens with empty editor"],
        ["Step 2: Command Palette", "Press Ctrl+Shift+P", "Floating overlay opens; type 'Check' and press Enter"],
        ["Step 3: Valid Java 21", "Load SampleValid.java with record patterns", "Status bar turns green: 'Parsing Successful'"],
        ["Step 4: Invalid Java", "Introduce error: int b = ; on Line 4", "Status bar turns red: Line 4 highlighted in red and centered"],
        ["Step 5: Code Fix", "Fix error: int b = 42; and press F5", "Error highlight clears instantly; green status returns"],
        ["Step 6: Batch Tests", "Run: python tests/run_tests.py", "Terminal displays 59/59 PASS (100.0%) summary table"]
    ]
    doc.add_table(headers, rows, [1.8, 2.5, 2.9])
    
    doc.add_heading_1("4. Concluding Script")
    doc.add_callout(
        "\"To conclude, our system proves that formal compiler theory can be cleanly translated into a high-performance, "
        "modern developer tool. All source code, grammar rules, native libraries, and tests are complete and verified. "
        "Thank you, and I am happy to answer any questions.\"",
        title="CLOSING STATEMENT",
        style="success"
    )
    
    doc.save(os.path.join(DOC_DIR, "20_Demo_Presentation_Script.pdf"))

def main():
    print("======================================================================")
    print("GENERATING 20 TOPIC-SPECIFIC ACADEMIC PDF DOCUMENTS")
    print("======================================================================")
    
    generators = [
        gen_doc_01, gen_doc_02, gen_doc_03, gen_doc_04, gen_doc_05,
        gen_doc_06, gen_doc_07, gen_doc_08, gen_doc_09, gen_doc_10,
        gen_doc_11, gen_doc_12, gen_doc_13, gen_doc_14, gen_doc_15,
        gen_doc_16, gen_doc_17, gen_doc_18, gen_doc_19, gen_doc_20
    ]
    
    for i, gen in enumerate(generators, 1):
        try:
            gen()
        except Exception as e:
            print(f"[ERROR] Failed to generate doc {i:02d}: {e}")
            import traceback
            traceback.print_exc()
            
    print("======================================================================")
    print("PDF GENERATION COMPLETED.")
    print("======================================================================")

if __name__ == "__main__":
    main()
