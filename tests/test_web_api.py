import os
import io
import json
import unittest

# Ensure project root is in path
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.app import create_app

class TestWebAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

    def test_health_check(self):
        """Verify GET /api/health returns healthy and parser status."""
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertTrue(data.get("parser_ready"))

    def test_get_samples(self):
        """Verify GET /api/samples returns sample programs."""
        resp = self.client.get("/api/samples")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data.get("success"))
        samples = data.get("samples")
        self.assertIn("records_patterns", samples)
        self.assertIn("switch_guards", samples)
        self.assertIn("array_initializers", samples)

    def test_index_page_serves(self):
        """Verify GET / serves HTML page."""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Java 21 Syntax Checker", resp.data)
        self.assertIn(b"CodeMirror", resp.data)

    def test_valid_simple_class(self):
        """Verify checking a valid simple class returns 200 and valid=True."""
        code = "public class Simple { int x = 10; }"
        resp = self.client.post("/api/check", json={"code": code})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["valid"])
        self.assertIn("SUCCESS", data["message"])
        self.assertIsNone(data["line"])

    def test_valid_java21_record_pattern(self):
        """Verify checking Java 21 record pattern returns 200 and valid=True."""
        code = """
        public class RecordDemo {
            public record Point(double x, double y) {}
            void test(Object o) {
                if (o instanceof Point(double x, double y)) {
                    System.out.println(x + y);
                }
            }
        }
        """
        resp = self.client.post("/api/check", json={"code": code})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["valid"])

    def test_valid_java21_switch_when_guard(self):
        """Verify checking Java 21 switch with when guard returns valid=True."""
        code = """
        public class SwitchDemo {
            String eval(Object o) {
                return switch (o) {
                    case null -> "null";
                    case Integer i when i > 0 -> "positive";
                    default -> "other";
                };
            }
        }
        """
        resp = self.client.post("/api/check", json={"code": code})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["valid"])

    def test_valid_array_initializer(self):
        """Verify valid array initializers with trailing commas."""
        code = """
        public class ArrayDemo {
            String[] depts = {"CSE", "ECE", "IT",};
            int[][] matrix = {{1, 2}, {3, 4}};
        }
        """
        resp = self.client.post("/api/check", json={"code": code})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["valid"])

    def test_invalid_missing_semicolon(self):
        """Verify missing semicolon returns valid=False and line number."""
        code = """class Test {
            void run() {
                int a = 10
                int b = 20;
            }
        }"""
        resp = self.client.post("/api/check", json={"code": code})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertFalse(data["valid"])
        self.assertEqual(data["line"], 4)
        self.assertIn("ERROR", data["message"])

    def test_invalid_missing_closing_brace(self):
        """Verify unclosed class brace returns valid=False."""
        code = "class Test { int x = 10;"
        resp = self.client.post("/api/check", json={"code": code})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertFalse(data["valid"])
        self.assertIn("ERROR", data["message"])

    def test_invalid_missing_parenthesis(self):
        """Verify missing parenthesis returns valid=False."""
        code = "class Test { void run( { int x = 1; } }"
        resp = self.client.post("/api/check", json={"code": code})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertFalse(data["valid"])

    def test_invalid_double_semicolon_in_interface(self):
        """Verify double semicolon in interface declaration is rejected."""
        code = """interface Calculator {
            int calculate(int a, int b);;
        }"""
        resp = self.client.post("/api/check", json={"code": code})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertFalse(data["valid"])
        self.assertEqual(data["line"], 2)

    def test_comments_and_blank_lines_accuracy(self):
        """Verify line numbers remain accurate across comments and blank lines."""
        code = """// Multi-line comment
// Another comment line

class Test {

    // Blank line above
    int invalid = ;
}"""
        resp = self.client.post("/api/check", json={"code": code})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertFalse(data["valid"])
        self.assertEqual(data["line"], 7)

    def test_empty_submission(self):
        """Verify empty code submission returns HTTP 400."""
        resp = self.client.post("/api/check", json={"code": "   "})
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertFalse(data["valid"])
        self.assertIn("empty", data["message"].lower())

    def test_missing_code_field(self):
        """Verify request without 'code' or 'file' returns HTTP 400."""
        resp = self.client.post("/api/check", json={"other": "value"})
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertFalse(data["valid"])

    def test_malformed_json_body(self):
        """Verify malformed JSON returns HTTP 400."""
        resp = self.client.post(
            "/api/check",
            data="not valid json",
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(resp.status_code, 400)

    def test_file_upload_valid(self):
        """Verify multipart file upload of a valid .java file."""
        code = b"public class UploadedTest { int val = 42; }"
        file_obj = (io.BytesIO(code), "UploadedTest.java")
        resp = self.client.post(
            "/api/check",
            data={"file": file_obj},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["valid"])

    def test_file_upload_invalid(self):
        """Verify multipart file upload of an invalid .java file."""
        code = b"public class UploadedTest { int val = ; }"
        file_obj = (io.BytesIO(code), "UploadedTest.java")
        resp = self.client.post(
            "/api/check",
            data={"file": file_obj},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertFalse(data["valid"])
        self.assertEqual(data["line"], 1)

    def test_file_upload_wrong_extension(self):
        """Verify non-java file upload is rejected with 400."""
        file_obj = (io.BytesIO(b"binary"), "test.exe")
        resp = self.client.post(
            "/api/check",
            data={"file": file_obj},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn(".java", data["message"])

    def test_consecutive_requests_stability(self):
        """Verify parser state resets cleanly across multiple consecutive requests."""
        codes = [
            ("class A { int x = 1; }", True),
            ("class B { int y = ; }", False),
            ("class C { void f() {} }", True),
            ("class D { int z = ; }", False),
            ("class E { record R(int a) {} }", True),
        ]
        for src, expected in codes:
            resp = self.client.post("/api/check", json={"code": src})
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json()["valid"], expected)

if __name__ == "__main__":
    unittest.main()
