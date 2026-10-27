import os
import re
import sys
import time
import tempfile
import subprocess
import ctypes
from typing import Dict, Any, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ParserBridge:
    """
    Bridge to the native GNU Flex + Bison LALR(1) Java 21 syntax checker.
    Supports both direct C library invocation via ctypes (Linux .so / Windows .dll)
    and robust subprocess invocation (Linux ELF binary / Windows .exe).
    """

    def __init__(self):
        self.project_dir = BASE_DIR
        self.exe_path = None
        self.dll_path = None
        self.checker_lib = None
        self.use_dll = False
        self._discover_engine()

    def _discover_engine(self):
        """Locate native shared library or executable on the host system."""
        # Check environment variable first
        env_bin = os.environ.get("JAVACHECK_BIN")
        if env_bin and os.path.exists(env_bin):
            self.exe_path = os.path.abspath(env_bin)

        # 1. Search for shared library (.so on Linux, .dll on Windows)
        so_candidate = os.path.join(self.project_dir, "javacheck.so")
        dll_candidate = os.path.join(self.project_dir, "javacheck.dll")

        if os.path.exists(so_candidate):
            self.dll_path = so_candidate
        elif os.path.exists(dll_candidate):
            self.dll_path = dll_candidate

        if self.dll_path:
            try:
                lib = ctypes.CDLL(self.dll_path)
                lib.check_syntax.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
                lib.check_syntax.restype = ctypes.c_int
                self.checker_lib = lib
                self.use_dll = True
            except Exception:
                self.checker_lib = None
                self.use_dll = False

        # 2. Search for standalone executable
        if not self.exe_path:
            candidates = [
                os.path.join(self.project_dir, "javacheck"),       # Linux ELF
                os.path.join(self.project_dir, "javacheck.exe"),   # Windows EXE
                r"C:\msys64\ucrt64\bin\javacheck.exe",              # MSYS2 UCRT64
            ]
            for c in candidates:
                if os.path.exists(c):
                    self.exe_path = os.path.abspath(c)
                    break

    def is_ready(self) -> bool:
        """Return True if at least one execution backend is available."""
        return (self.use_dll and self.checker_lib is not None) or (self.exe_path is not None)

    def check_file(self, filepath: str, timeout: float = 5.0) -> Dict[str, Any]:
        """
        Check syntax of a .java file on disk.
        Returns a dictionary with keys: valid, line, token, message, exit_code, elapsed_ms.
        """
        abs_path = os.path.abspath(filepath)
        if not os.path.exists(abs_path):
            return {
                "valid": False,
                "line": None,
                "token": None,
                "message": f"File '{filepath}' not found",
                "exit_code": 2,
                "elapsed_ms": 0.0
            }

        start_time = time.perf_counter()
        raw_msg = ""
        exit_code = 1

        # Strategy 1: Shared Library (ctypes) - Fast, in-process
        if self.use_dll and self.checker_lib is not None:
            try:
                buf = ctypes.create_string_buffer(2048)
                exit_code = self.checker_lib.check_syntax(abs_path.encode('utf-8'), buf, 2048)
                raw_msg = buf.value.decode('utf-8', errors='replace').strip()
            except Exception as e:
                # Fall back to subprocess if ctypes encountered an issue
                raw_msg = ""
                exit_code = 1

        # Strategy 2: Standalone Executable (subprocess) - Isolated, safe
        if not raw_msg and self.exe_path:
            try:
                # Never use shell=True to prevent shell injection vulnerabilities
                p = subprocess.run(
                    [self.exe_path, abs_path],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                exit_code = p.returncode
                raw_msg = (p.stdout + "\n" + p.stderr).strip()
            except subprocess.TimeoutExpired:
                elapsed_ms = (time.perf_counter() - start_time) * 1000
                return {
                    "valid": False,
                    "line": None,
                    "token": None,
                    "message": f"ERROR: Syntax parser timed out after {timeout} seconds",
                    "exit_code": 124,
                    "elapsed_ms": round(elapsed_ms, 2)
                }
            except OSError as e:
                # Windows AppLocker/Device Guard fallback via cmd.exe
                if sys.platform == "win32":
                    try:
                        p = subprocess.run(
                            ['cmd.exe', '/c', self.exe_path, abs_path],
                            capture_output=True,
                            text=True,
                            timeout=timeout
                        )
                        exit_code = p.returncode
                        raw_msg = (p.stdout + "\n" + p.stderr).strip()
                    except Exception as inner_e:
                        raw_msg = f"ERROR: Execution failed: {str(inner_e)}"
                        exit_code = 2
                else:
                    raw_msg = f"ERROR: Parser execution failed: {str(e)}"
                    exit_code = 2

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        # Parse message
        return self._format_result(exit_code, raw_msg, elapsed_ms)

    def check_code_string(self, code: str, timeout: float = 5.0) -> Dict[str, Any]:
        """
        Check syntax of a raw Java code string.
        Safely creates a temporary .java file and ensures guaranteed cleanup.
        """
        if not code or not code.strip():
            return {
                "valid": False,
                "line": None,
                "token": None,
                "message": "ERROR: Source code is empty.",
                "exit_code": 1,
                "elapsed_ms": 0.0
            }

        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile('w', suffix='.java', delete=False, encoding='utf-8') as f:
                f.write(code)
                tmp_path = f.name
            return self.check_file(tmp_path, timeout=timeout)
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

    def _format_result(self, exit_code: int, raw_msg: str, elapsed_ms: float) -> Dict[str, Any]:
        """Parse the Flex/Bison parser output into a clean, structured dictionary."""
        is_valid = (exit_code == 0) and ("SUCCESS" in raw_msg or "Valid Java Syntax" in raw_msg)

        err_line = None
        err_token = None

        if not is_valid:
            # Pattern: ERROR: Line (\d+): Syntax error near '([^']*)'
            m = re.search(r"Line\s+(\d+)", raw_msg, re.IGNORECASE)
            if m:
                try:
                    err_line = int(m.group(1))
                except ValueError:
                    err_line = None

            t_match = re.search(r"near\s+'([^']*)'", raw_msg)
            if t_match:
                err_token = t_match.group(1)

        cleaned_msg = raw_msg
        if not cleaned_msg:
            cleaned_msg = "SUCCESS: Valid Java Syntax" if is_valid else "ERROR: Syntax error detected."

        return {
            "valid": is_valid,
            "line": err_line,
            "token": err_token,
            "message": cleaned_msg,
            "exit_code": exit_code,
            "elapsed_ms": round(elapsed_ms, 2)
        }

# Global singleton bridge instance
bridge = ParserBridge()
