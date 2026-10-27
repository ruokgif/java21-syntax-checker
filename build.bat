@echo off

echo ======================================================================
echo Java 21 Syntax Checker - Build Script (Windows CMD)
echo ======================================================================

:: Ensure MSYS2 UCRT64 / USR bin are in PATH if available
if exist C:\msys64\ucrt64\bin (
    set PATH=C:\msys64\ucrt64\bin;C:\msys64\usr\bin;%PATH%
)

echo [1/4] Checking required tools: flex, bison, gcc...
where flex >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 'flex' not found in PATH.
    exit /b 1
)

where bison >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 'bison' not found in PATH.
    exit /b 1
)

where gcc >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 'gcc' not found in PATH.
    exit /b 1
)

echo [2/4] Generating LALR(1) Parser with GNU Bison...
bison -v -d parser/java_parser.y --report-file=parser/java_parser.output -o parser/java_parser.tab.c
if errorlevel 1 (
    echo [ERROR] Bison generation failed.
    exit /b 1
)

echo [3/4] Generating Lexer with GNU Flex...
flex -o lexer/lex.yy.c lexer/java_lexer.l
if errorlevel 1 (
    echo [ERROR] Flex generation failed.
    exit /b 1
)

echo [4/4] Compiling javacheck.dll and javacheck.exe with GCC...
gcc -O2 -shared -Iparser -Ilexer parser/java_parser.tab.c lexer/lex.yy.c -o javacheck.dll
if errorlevel 1 (
    echo [ERROR] Compilation of javacheck.dll failed.
    exit /b 1
)

gcc -O2 -Iparser -Ilexer parser/java_parser.tab.c lexer/lex.yy.c -o javacheck.exe
if errorlevel 1 (
    echo [ERROR] Compilation of javacheck.exe failed.
    exit /b 1
)

echo.
echo ======================================================================
echo Build Complete!
echo Outputs:
echo   - javacheck.dll (Native C Library for GUI and Python ctypes)
echo   - javacheck.exe (Standalone CLI syntax checker executable)
echo ======================================================================
