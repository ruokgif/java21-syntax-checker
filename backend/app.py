import os
import sys
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.parser_bridge import bridge

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(PROJECT_ROOT, "templates"),
        static_folder=os.path.join(PROJECT_ROOT, "static")
    )

    # Enable CORS for cross-origin integration if required
    CORS(app)

    # Maximum upload size: 2 Megabytes
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

    # -------------------------------------------------------------------------
    # Preset Java 21 Code Samples
    # -------------------------------------------------------------------------
    SAMPLE_PROGRAMS = {
        "records_patterns": {
            "title": "Java 21: Records & Pattern Matching",
            "code": """// Java 21: Record Patterns and instanceof Deconstruction
public class RecordPatternDemo {
    public record Point(double x, double y) {}
    public record ColoredPoint(Point p, String color) {}

    public static void printPoint(Object obj) {
        if (obj instanceof ColoredPoint(Point(double x, double y), String c)) {
            System.out.println("Point at (" + x + ", " + y + ") with color " + c);
        } else if (obj instanceof Point(double x, double y)) {
            System.out.println("Point at (" + x + ", " + y + ")");
        }
    }

    public static void main(String[] args) {
        ColoredPoint cp = new ColoredPoint(new Point(3.5, 4.2), "Cyan");
        printPoint(cp);
    }
}"""
        },
        "switch_guards": {
            "title": "Java 21: Pattern Matching for Switch & When Guards",
            "code": """// Java 21: Switch Expressions with Type Patterns & When Guards
public class SwitchGuardsDemo {
    public static String classify(Object obj) {
        return switch (obj) {
            case null -> "Null reference";
            case Integer i when i < 0 -> "Negative integer: " + i;
            case Integer i when i == 0 -> "Zero";
            case Integer i -> "Positive integer: " + i;
            case String s when s.isEmpty() -> "Empty string";
            case String s -> "String of length " + s.length();
            default -> "Other type: " + obj.toString();
        };
    }

    public static void main(String[] args) {
        System.out.println(classify(-42));
        System.out.println(classify("Java 21"));
    }
}"""
        },
        "array_initializers": {
            "title": "Array Initializers & Multi-Dimensional",
            "code": """// Java: Multi-dimensional and Sized Array Initializers
public class ArrayInitializerDemo {
    private String[] departments = {
        "Computer Science",
        "Electronics",
        "Information Tech",
        "Electrical"
    };

    private int[][] matrix = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    public void display() {
        String[] copy = new String[] {"Alpha", "Beta", "Gamma"};
        int[] empty = {};
        System.out.println("Departments: " + departments.length);
        System.out.println("Matrix center: " + matrix[1][1]);
    }

    public static void main(String[] args) {
        new ArrayInitializerDemo().display();
    }
}"""
        },
        "sealed_hierarchy": {
            "title": "Java 17/21: Sealed Classes & Interfaces",
            "code": """// Java 17+: Sealed Hierarchy with Permits
public sealed interface Shape permits Circle, Rectangle, Square {}

final class Circle implements Shape {
    private final double radius;
    public Circle(double r) { this.radius = r; }
    public double radius() { return radius; }
}

sealed class Rectangle implements Shape permits Square {
    final double width, height;
    public Rectangle(double w, double h) { this.width = w; this.height = h; }
}

final class Square extends Rectangle {
    public Square(double side) { super(side, side); }
}"""
        },
        "syntax_error_demo": {
            "title": "Syntax Error Demo (Missing Semicolon & Token Error)",
            "code": """// Sample with intentional syntax errors for verification
public class ErrorDemo {
    public static void main(String[] args) {
        int a = 10;
        int b = 20;

        // Intentional error: missing semicolon on the line below
        int sum = a + b

        System.out.println("Sum is: " + sum);
    }
}"""
        }
    }

    # -------------------------------------------------------------------------
    # Routes
    # -------------------------------------------------------------------------
    @app.route("/")
    def index():
        """Serve the modern syntax checker single-page interface."""
        return render_template("index.html")

    @app.route("/api/health", methods=["GET"])
    def health():
        """Health check endpoint for Render service monitoring."""
        return jsonify({
            "status": "healthy",
            "service": "Java 21 Syntax Checker",
            "engine": "GNU Flex + Bison LALR(1)",
            "parser_ready": bridge.is_ready(),
            "use_dll": bridge.use_dll,
            "exe_path": bridge.exe_path
        }), 200

    @app.route("/api/samples", methods=["GET"])
    def samples():
        """Retrieve preset Java 21 code snippets."""
        return jsonify({
            "success": True,
            "samples": SAMPLE_PROGRAMS
        }), 200

    @app.route("/api/check", methods=["POST"])
    def check_syntax():
        """
        Check Java source code syntax.
        Accepts:
          - JSON payload: { "code": "..." }
          - Multipart file upload: file: <.java file>
          - URL-encoded form data: code: "..."
        """
        code = None

        # 1. Check for file upload
        if "file" in request.files:
            file_item = request.files["file"]
            if file_item.filename == "":
                return jsonify({
                    "valid": False,
                    "error": "No file selected",
                    "message": "ERROR: Uploaded file has no name."
                }), 400

            if not file_item.filename.lower().endswith((".java", ".txt")):
                return jsonify({
                    "valid": False,
                    "error": "Invalid file type",
                    "message": "ERROR: File must have a .java extension."
                }), 400

            try:
                raw_bytes = file_item.read()
                code = raw_bytes.decode("utf-8", errors="replace")
            except Exception as e:
                return jsonify({
                    "valid": False,
                    "error": "File read failure",
                    "message": f"ERROR: Could not read uploaded file: {str(e)}"
                }), 400

        # 2. Check for JSON payload
        elif request.is_json:
            data = request.get_json(silent=True)
            if not data or not isinstance(data, dict):
                return jsonify({
                    "valid": False,
                    "error": "Malformed request",
                    "message": "ERROR: Invalid JSON request body."
                }), 400
            code = data.get("code")

        # 3. Check for standard form POST
        elif request.form and "code" in request.form:
            code = request.form.get("code")

        # Validate code input
        if code is None:
            return jsonify({
                "valid": False,
                "error": "Missing input",
                "message": "ERROR: Request must contain 'code' string or a 'file' upload."
            }), 400

        if not code.strip():
            return jsonify({
                "valid": False,
                "line": None,
                "token": None,
                "error": "Empty source",
                "message": "ERROR: Java source code cannot be empty.",
                "exit_code": 1,
                "elapsed_ms": 0.0
            }), 400

        # Run syntax analysis through the Flex/Bison parser bridge
        try:
            result = bridge.check_code_string(code)
            # HTTP 200 for completed check, regardless of whether syntax is valid or has errors
            return jsonify(result), 200
        except Exception as e:
            return jsonify({
                "valid": False,
                "line": None,
                "token": None,
                "error": "Internal parser error",
                "message": f"ERROR: Syntax checker encountered an internal error: {str(e)}",
                "exit_code": 2,
                "elapsed_ms": 0.0
            }), 500

    # -------------------------------------------------------------------------
    # HTTP Error Handlers
    # -------------------------------------------------------------------------
    @app.errorhandler(RequestEntityTooLarge)
    def handle_oversized_payload(e):
        return jsonify({
            "valid": False,
            "error": "Payload too large",
            "message": "ERROR: Submitted Java source exceeds the 2MB size limit."
        }), 413

    @app.errorhandler(404)
    def handle_not_found(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Endpoint not found", "path": request.path}), 404
        return render_template("index.html"), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({"error": "HTTP method not allowed on this endpoint"}), 405

    @app.errorhandler(500)
    def handle_internal_server_error(e):
        return jsonify({"error": "Internal server error occurred"}), 500

    return app

# Main entry point for WSGI and Render (gunicorn backend.app:app)
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
