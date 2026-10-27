import os
import sys
import subprocess

exe_path = os.path.abspath("javacheck.exe")
msys_exe = r"C:\msys64\ucrt64\bin\javacheck.exe"
if os.path.exists(msys_exe):
    exe_path = msys_exe
dll_path = os.path.abspath("javacheck.dll")

use_dll = False
checker_lib = None

if os.path.exists(dll_path):
    try:
        import ctypes
        checker_lib = ctypes.CDLL(dll_path)
        checker_lib.check_syntax.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        checker_lib.check_syntax.restype = ctypes.c_int
        use_dll = True
    except Exception:
        use_dll = False

def check_file(filepath):
    abs_path = os.path.abspath(filepath)
    if use_dll and checker_lib is not None:
        import ctypes
        buffer = ctypes.create_string_buffer(1024)
        ret = checker_lib.check_syntax(abs_path.encode('utf-8'), buffer, 1024)
        msg = buffer.value.decode('utf-8')
        return ret, msg
    else:
        try:
            p = subprocess.run([exe_path, abs_path], capture_output=True, text=True)
        except OSError:
            p = subprocess.run(['cmd.exe', '/c', exe_path, abs_path], capture_output=True, text=True)
        out = (p.stdout + p.stderr).strip()
        return p.returncode, out

test_files = [
    ("tests/valid_1.java", True, "Minimal class"),
    ("tests/valid_2.java", True, "Public class"),
    ("tests/valid_3.java", True, "Class with field"),
    ("tests/valid_4.java", True, "Class with method and assignment"),
    ("tests/valid_full.java", True, "Full Java 17 features (records, switch, lambdas, generics)"),
    ("tests/test_interface.java", True, "Interface with generic method"),
    ("tests/test_expr.java", True, "Method call statement"),
    ("tests/test_for.java", True, "For loop statement"),
    ("tests/test_advanced.java", True, "Sealed interfaces, records, enums, varargs, yield"),
    ("tests/unicode_test.java", True, "Unicode identifier program"),
    ("tests/java21_record_patterns.java", True, "Java 21 Record patterns: instanceof, nested, var, generic"),
    ("tests/java21_switch_patterns.java", True, "Java 21 Switch: type patterns, record patterns, when guards, null"),
    ("tests/test_phase5b_regressions.java", True, "Phase 5B regressions: sealed, lambdas, parenthesized expr, switch guards"),
    ("tests/invalid_1.java", False, "Unclosed class body"),
    ("tests/invalid_2.java", False, "Missing expression after '='"),
    ("tests/invalid_3.java", False, "Missing ')' in method parameters"),
    ("tests/invalid_4.java", False, "Missing ')' in if condition"),
    ("tests/invalid_5.java", False, "Missing semicolon on line 5"),
    ("tests/invalid_6.java", False, "Missing ')' in if condition"),
    ("tests/invalid_7.java", False, "Missing semicolon between statements"),
    ("tests/invalid_java21_1.java", False, "Invalid Java 21: missing expression after when guard"),
    ("tests/invalid_java21_2.java", False, "Invalid Java 21: unclosed record pattern parenthesis"),
    ("tests/invalid_java21_3.java", False, "Invalid Java 21: illegal when in if statement"),
    ("tests/err_line_1.java", False, "Phase 6 error: line 1 error"),
    ("tests/err_line_2.java", False, "Phase 6 error: line 2 error"),
    ("tests/err_line_5.java", False, "Phase 6 error: line 5 error"),
    ("tests/err_blank_lines.java", False, "Phase 6 error: line 7 error after blank lines"),
    ("tests/err_single_comment.java", False, "Phase 6 error: line 6 error after single comment"),
    ("tests/err_multi_comment.java", False, "Phase 6 error: line 8 error after multi-line comment"),
    ("tests/err_missing_brace.java", False, "Phase 6 error: missing brace at EOF"),
    ("tests/err_missing_paren.java", False, "Phase 6 error: missing paren on line 3"),
    ("tests/err_missing_bracket.java", False, "Phase 6 error: missing bracket on line 3"),
    ("tests/err_missing_semi.java", False, "Phase 6 error: missing semicolon on line 4"),
    ("tests/err_missing_comma.java", False, "Phase 6 error: missing comma on line 2"),
    ("tests/err_text_block.java", False, "Phase 6 error: line 7 error after text block"),
    ("tests/test_urshift_assign.java", True, "Phase 9: Unsigned right shift assignment (>>>=)"),
    ("tests/test_module_info.java", True, "Phase 9: Module declaration (module-info.java)"),
    ("tests/test_try_resources_multi.java", True, "Phase 9: Multiple try-with-resources with trailing semicolon"),
    ("tests/test_array_ragged.java", True, "Phase 9: Multidimensional and ragged arrays"),
    ("tests/test_generic_constructor.java", True, "Phase 9: Explicit generic constructor calls"),
    ("tests/test_annotation_arrays.java", True, "Phase 9: Annotation array attributes"),
    ("tests/test_record_compact_annotated.java", True, "Phase 9: Annotated compact record constructor and nested patterns"),
    ("tests/err_empty_char.java", False, "Phase 9 error: empty character literal"),
    ("tests/err_accuracy_line1.java", False, "Phase 10: Error on Line 1"),
    ("tests/err_accuracy_line2.java", False, "Phase 10: Error on Line 2"),
    ("tests/err_accuracy_middle.java", False, "Phase 10: Error in method body on Line 4"),
    ("tests/err_accuracy_after_blank.java", False, "Phase 10: Error after multiple blank lines on Line 8"),
    ("tests/err_accuracy_after_single_comment.java", False, "Phase 10: Error after single-line comments on Line 9"),
    ("tests/err_accuracy_after_block_comment.java", False, "Phase 10: Error after block comment on Line 9"),
    ("tests/err_accuracy_after_text_block.java", False, "Phase 10: Error after text block on Line 7"),
    ("tests/err_accuracy_missing_semicolon.java", False, "Phase 10: Lookahead error on Line 4 due to missing semicolon"),
    ("tests/err_accuracy_missing_closing_paren.java", False, "Phase 10: Missing closing paren on Line 3"),
    ("tests/err_accuracy_missing_closing_bracket.java", False, "Phase 10: Missing closing bracket on Line 3"),
    ("tests/err_accuracy_missing_closing_brace.java", False, "Phase 10: Missing closing brace on Line 7"),
    ("tests/err_accuracy_unexpected_token.java", False, "Phase 10: Unexpected token on Line 4"),
    ("tests/err_accuracy_eof.java", False, "Phase 10: Abrupt EOF error"),
    ("tests/err_stress_record_pattern.java", False, "Phase 10 Stress: Error in nested record deconstruction on Line 6"),
    ("tests/err_stress_nested_generic.java", False, "Phase 10 Stress: Error in generic lambda body on Line 7"),
    ("tests/err_stress_switch_guard.java", False, "Phase 10 Stress: Missing switch guard expression on Line 7"),
    ("tests/test_array_initializers.java", True, "Array initializers: basic, empty, trailing comma, nested, new Type[] {}"),
    ("tests/err_invalid_array_init.java", False, "Invalid array initializer: consecutive commas"),
    ("tests/err_double_semicolon.java", False, "Double semicolon in interface declaration rejected")
]

print("=" * 70)
print("JAVA SYNTAX CHECKER TEST SUITE (FLEX + BISON LALR(1))")
print("=" * 70)

passed = 0
total = len(test_files)

for path, should_be_valid, desc in test_files:
    ret, msg = check_file(path)
    is_valid = (ret == 0)
    test_passed = (is_valid == should_be_valid)
    status_icon = "PASS" if test_passed else "FAIL"
    if test_passed:
        passed += 1
    print(f"[{status_icon}] {path:<45} | Expected: {'VALID' if should_be_valid else 'INVALID':<7} | Result: {msg}")

print("=" * 70)
print(f"Summary: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
print("=" * 70)

if passed != total:
    sys.exit(1)
