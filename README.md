# Java 21 Syntax Checker — Web Application & Render Deployment

A production-ready compiler design project implementing a high-precision formal syntax checker for the **Java 21 (LTS)** programming language. Powered by **GNU Flex**, **GNU Bison LALR(1)**, **C99/GCC**, a **Python Flask** backend, and a modern web interface.

---

## 1. Project Overview & Objective

The objective of this project is to construct a formal front-end syntax verification engine for Java 21 source files (`.java`). It determines whether an input Java program is syntactically well-formed according to the Java Language Specification (JLS 21). When an input program violates grammar rules, the engine pinpoint-locates the precise source line where the syntax error was encountered and displays diagnostic details (line number, offending token, and error message).

Users can:
1. **Interactive Web App**: Enter or paste Java code, choose from curated Java 21 samples, or upload `.java` files in their browser.
2. **Desktop Application**: Run the Python Tkinter GUI natively on Windows/Linux.
3. **Command Line Interface (CLI)**: Run `javacheck <file.java>` directly in CI/CD or terminals.

> **Scope Note**: This project is a **syntax checker and parser**, not a complete compiler. It does not perform semantic analysis (type checking, symbol table resolution), does not generate bytecode, and never executes submitted code.

---

## 2. System Architecture

```text
+-----------------------------------------------------------------------------------+
|                           Client Interface Options                                |
|  - Modern Web Browser (CodeMirror, Dark Theme, Drag & Drop, Keyboard Shortcuts)   |
|  - Desktop Python Tkinter GUI (gui/app.py)                                        |
|  - Command Line Interface (javacheck CLI)                                         |
+-----------------------------------------------------------------------------------+
                                          |
                                          v  HTTP POST /api/check (Web)
+-----------------------------------------------------------------------------------+
|                         Python Flask Web Backend (backend/app.py)                 |
|  - Validates payload size (Max 2MB) & MIME type                                   |
|  - Safe subprocess/ctypes invocation without shell=True                           |
|  - Automatic temporary file lifecycle & guaranteed cleanup                       |
+-----------------------------------------------------------------------------------+
                                          |
                                          v  ctypes FFI or Native Subprocess
+-----------------------------------------------------------------------------------+
|                         GNU Flex 2.6.x Lexical Analyzer                           |
|  - lexer/java_lexer.l                                                             |
|  - Tracks yylloc line/column coordinates via YY_USER_ACTION                       |
|  - Tokenizes Java 21 keywords, record patterns, switch guards, text blocks        |
+-----------------------------------------------------------------------------------+
                                          | Token Stream (Tokens + Locations)
                                          v
+-----------------------------------------------------------------------------------+
|                        GNU Bison 3.8.x LALR(1) Syntax Parser                      |
|  - parser/java_parser.y                                                           |
|  - Deterministic shift-reduce LALR(1) state automaton                             |
|  - Custom yyerror() capturing line numbers and near tokens                        |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
                     +-----------------------------------------+
                     | Exit Code 0: SUCCESS: Valid Java Syntax |
                     | Exit Code 1: ERROR: Line X: near 'tok'  |
                     +-----------------------------------------+
```

---

## 3. Java 21 Grammar Capabilities

- **Record Patterns & Deconstruction**: `record Point(int x, int y) {}`, `if (obj instanceof Point(var x, var y))`
- **Pattern Matching for `switch`**: Type patterns, Record patterns, `case null, default`
- **Switch Guards**: Contextual `when` expressions (`case Point(x, y) when x > 0 -> ...`)
- **Sealed Classes & Interfaces**: `sealed`, `non-sealed`, `permits` clauses
- **Array Initializers**: Direct brace initializers (`String[] v = {"A", "B",};`), sized expressions (`new String[] {"A"}`), multi-dimensional/ragged arrays (`int[][] m = {{1, 2}, {3, 4}};`)
- **Text Blocks**: `"""..."""` multi-line string literals
- **Lambdas & Method References**: `(a, b) -> a + b`, `String::length`, `System.out::println`
- **Generics & Diamond Operator**: `List<Map<String, List<Integer>>>`, explicit constructor type arguments
- **Local Variable Type Inference**: `var list = new ArrayList<String>();`
- **Annotations & Modules**: `@Override`, custom annotations, `module-info.java`

---

## 4. Project Directory Structure

```text
├── lexer/
│   ├── java_lexer.l              # Flex lexical specification with line tracking
│   ├── tokens.h                  # Token enumeration definitions
│   └── lexer_driver.c            # Standalone lexer debugging driver
├── parser/
│   ├── java_parser.y             # Bison LALR(1) Java 21 grammar specification
│   ├── java_parser.tab.c         # Bison-generated C parser
│   └── java_parser.tab.h         # Bison-generated token header
├── backend/
│   ├── __init__.py
│   ├── parser_bridge.py          # Unified ctypes / subprocess bridge
│   └── app.py                    # Flask Web Server & API endpoints
├── templates/
│   └── index.html                # Responsive web app template
├── static/
│   ├── css/
│   │   └── style.css             # Terminal-native dark design system
│   └── js/
│       └── app.js                # CodeMirror & interactive client logic
├── gui/
│   └── app.py                    # Python Tkinter desktop GUI
├── tests/
│   ├── run_tests.py              # 62-test comprehensive grammar test suite
│   ├── test_web_api.py           # 19-test Flask Web API automated test suite
│   ├── test_gui_backend.py       # 14-test Tkinter GUI backend test suite
│   └── test_pairing_features.py  # 14-test editor pairing feature suite
├── Dockerfile                    # Multi-stage Linux build for Render
├── .dockerignore                 # Excludes local artifacts from build context
├── requirements.txt              # Production Python dependencies (Flask, Gunicorn)
├── render.yaml                   # Render Infrastructure as Code Blueprint
├── build.sh                      # Linux compilation script
├── build.bat                     # Windows compilation batch script
├── Makefile                      # Cross-platform build automation
└── README.md                     # Complete project documentation
```

---

## 5. Local Execution Instructions

### Prerequisites
- **Python 3.10+**
- **GCC / MinGW-w64**
- **GNU Flex 2.6+**
- **GNU Bison 3.8+**

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Build the Parser
- **On Windows (CMD / MSYS2)**:
  ```cmd
  build.bat
  ```
- **On Linux / macOS**:
  ```bash
  chmod +x build.sh
  ./build.sh
  ```
  *or with Make:*
  ```bash
  make linux
  ```

### Step 3: Run Automated Tests
```bash
# 1. Run core grammar tests (62 tests)
python tests/run_tests.py

# 2. Run Web API tests (19 tests)
python tests/test_web_api.py

# 3. Run GUI backend tests (14 tests)
python tests/test_gui_backend.py
```

### Step 4: Launch the Web Application
```bash
python backend/app.py
```
Open your browser to: **`http://127.0.0.1:5000`**

### Step 5: (Optional) Launch Desktop GUI
```bash
python gui/app.py
```

---

## 6. Web API Specification

### `POST /api/check`
Analyzes submitted Java source code and returns syntax diagnostics.

- **Request Body (JSON)**:
  ```json
  {
    "code": "public class HelloWorld { public static void main(String[] args) { System.out.println(\"Hello\"); } }"
  }
  ```
- **Request Body (Multipart File Upload)**:
  - Key: `file`
  - Value: `<filename>.java` file
- **Success Response (HTTP 200)**:
  ```json
  {
    "valid": true,
    "line": null,
    "token": null,
    "message": "SUCCESS: Valid Java Syntax",
    "exit_code": 0,
    "elapsed_ms": 0.42
  }
  ```
- **Error Response (HTTP 200)**:
  ```json
  {
    "valid": false,
    "line": 4,
    "token": "int",
    "message": "ERROR: Line 4: Syntax error near 'int'",
    "exit_code": 1,
    "elapsed_ms": 0.19
  }
  ```
- **Client Error (HTTP 400)**:
  ```json
  {
    "valid": false,
    "error": "Empty source",
    "message": "ERROR: Java source code cannot be empty."
  }
  ```

### `GET /api/health`
Returns health check and parser engine readiness.
```json
{
  "status": "healthy",
  "service": "Java 21 Syntax Checker",
  "engine": "GNU Flex + Bison LALR(1)",
  "parser_ready": true
}
```

---

## 7. Render Deployment Guide (Step-by-Step)

This application is containerized using Docker, allowing it to compile the C parser on Linux and run via Gunicorn on **Render's Free Web Service Tier**.

### Step 1: Push Code to GitHub
1. Initialize a git repository if you haven't already:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Java 21 Syntax Checker Web App"
   ```
2. Create a new repository on [GitHub](https://github.com/new).
3. Push your repository:
   ```bash
   git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY>.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Log in to Render
1. Visit [https://render.com](https://render.com) and sign in (using GitHub is recommended).

### Step 3: Create a New Web Service
1. In the Render Dashboard, click the **New +** button in the top right.
2. Select **Web Service**.
3. Choose **Build and deploy from a Git repository** and click **Next**.

### Step 4: Connect Your GitHub Repository
1. Select your GitHub repository (`<YOUR_REPOSITORY>`).
2. Click **Connect**.

### Step 5: Configure the Web Service
Configure the following settings:
- **Name**: `java21-syntax-checker` (or your preferred name)
- **Region**: Choose the closest region (e.g., `Oregon (US West)` or `Frankfurt (EU)`)
- **Branch**: `main`
- **Runtime**: **Docker** *(Render will automatically detect the `Dockerfile` in the root directory)*
- **Instance Type**: **Free**

### Step 6: Configure Environment Variables
Under the **Environment Variables** section, ensure the following is set:
- `PORT` = `5000` *(Render sets this automatically, but confirming it ensures smooth binding)*

### Step 7: Deploy the Service
1. Click **Create Web Service** at the bottom of the page.
2. Render will automatically:
   - Pull your repository.
   - Build the Docker image.
   - Install Debian packages (`gcc`, `flex`, `bison`, `make`).
   - Run Flex and Bison to compile `javacheck` and `javacheck.so`.
   - Install Python requirements (`Flask`, `Gunicorn`).
   - Start Gunicorn on port `5000`.

### Step 8: View Live URL & Verification
1. Once the deployment finishes, the status will show **Live**.
2. Click the public URL at the top left of the dashboard (e.g., `https://java21-syntax-checker.onrender.com`).
3. The Java 21 Syntax Checker web interface will load with sample programs ready for testing.

### Step 9: Inspecting Logs
1. Click the **Logs** tab in the Render dashboard to see live HTTP traffic, Gunicorn startup logs, and parser execution logs.

### Step 10: Troubleshooting
- **Build Failure during Bison/Flex:** Ensure `parser/java_parser.y` and `lexer/java_lexer.l` are committed and not listed in `.dockerignore`.
- **Port Binding Timeout:** Verify that `gunicorn` is binding to `0.0.0.0:$PORT` (already handled in our `Dockerfile`).
- **Free Tier Sleep:** On Render's free tier, the service spins down after 15 minutes of inactivity. The first request after sleep may take ~30 seconds to spin up.

### Step 11: Redeploying Updates
Whenever you push new commits to your GitHub `main` branch, Render will automatically rebuild and redeploy your service without any manual steps.
