# PowerShell Build Script for Java 21 Syntax Checker
$ErrorActionPreference = "Stop"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Java 21 Syntax Checker - Build Script (PowerShell)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Prepend MSYS2 paths if present
if (Test-Path "C:\msys64\ucrt64\bin") {
    $env:PATH = "C:\msys64\ucrt64\bin;C:\msys64\usr\bin;" + $env:PATH
}

Write-Host "[1/4] Checking required tools (flex, bison, gcc)..." -ForegroundColor Yellow
$tools = @("flex", "bison", "gcc")
foreach ($tool in $tools) {
    if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
        Write-Error "Required tool '$tool' not found in PATH."
        exit 1
    }
}

Write-Host "[2/4] Generating LALR(1) Parser with GNU Bison..." -ForegroundColor Yellow
bison -v -d parser/java_parser.y --report-file=parser/java_parser.output -o parser/java_parser.tab.c

Write-Host "[3/4] Generating Lexer with GNU Flex..." -ForegroundColor Yellow
flex -o lexer/lex.yy.c lexer/java_lexer.l

Write-Host "[4/4] Compiling javacheck.dll and javacheck.exe with GCC..." -ForegroundColor Yellow
gcc -O2 -shared -Iparser -Ilexer parser/java_parser.tab.c lexer/lex.yy.c -o javacheck.dll
gcc -O2 -Iparser -Ilexer parser/java_parser.tab.c lexer/lex.yy.c -o javacheck.exe

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "Build Complete!" -ForegroundColor Green
Write-Host "Outputs:" -ForegroundColor Green
Write-Host "  - javacheck.dll (Native C Library for GUI & Python ctypes integration)" -ForegroundColor Green
Write-Host "  - javacheck.exe (Standalone CLI syntax checker executable)" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
