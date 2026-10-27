#!/bin/bash
# =============================================================================
# Linux Build Script for Java 21 Syntax Checker (Flex + Bison + GCC)
# =============================================================================
set -e

echo "======================================================================"
echo "Java 21 Syntax Checker - Linux Build Script"
echo "======================================================================"

echo "[1/4] Checking tools..."
which bison >/dev/null || { echo "Error: bison not found"; exit 1; }
which flex >/dev/null || { echo "Error: flex not found"; exit 1; }
which gcc >/dev/null || { echo "Error: gcc not found"; exit 1; }

echo "[2/4] Generating LALR(1) Parser with Bison..."
bison -v -d parser/java_parser.y --report-file=parser/java_parser.output -o parser/java_parser.tab.c

echo "[3/4] Generating Lexer with Flex..."
flex -o lexer/lex.yy.c lexer/java_lexer.l

echo "[4/4] Compiling javacheck.so and javacheck executable..."
gcc -O2 -Wall -Wno-unused-function -shared -fPIC -Iparser -Ilexer parser/java_parser.tab.c lexer/lex.yy.c -o javacheck.so
gcc -O2 -Wall -Wno-unused-function -Iparser -Ilexer parser/java_parser.tab.c lexer/lex.yy.c -o javacheck
chmod +x javacheck

echo "======================================================================"
echo "Build Complete!"
echo "Outputs:"
echo "  - javacheck.so (Native Linux shared object for ctypes)"
echo "  - javacheck (Standalone Linux executable)"
echo "======================================================================"
