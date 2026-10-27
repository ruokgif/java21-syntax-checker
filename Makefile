# Makefile for Java 21 Syntax Checker (Flex + GNU Bison LALR(1) + GCC)

CC ?= gcc
CFLAGS ?= -O2 -Wall -Wno-unused-function
BISON ?= bison
FLEX ?= flex

PARSER_SRC = parser/java_parser.y
PARSER_TAB_C = parser/java_parser.tab.c
PARSER_TAB_H = parser/java_parser.tab.h
PARSER_OUTPUT = parser/java_parser.output

LEXER_SRC = lexer/java_lexer.l
LEXER_YY_C = lexer/lex.yy.c

DLL_TARGET = javacheck.dll
EXE_TARGET = javacheck.exe
SO_TARGET = javacheck.so
LINUX_EXE = javacheck

.PHONY: all linux clean test test-web web gui help

# Default for Windows/MSYS2
all: $(DLL_TARGET) $(EXE_TARGET)

# Linux target for Docker and Linux development
linux: $(SO_TARGET) $(LINUX_EXE)

$(PARSER_TAB_C) $(PARSER_TAB_H): $(PARSER_SRC)
	$(BISON) -v -d $(PARSER_SRC) --report-file=$(PARSER_OUTPUT) -o $(PARSER_TAB_C)

$(LEXER_YY_C): $(LEXER_SRC) $(PARSER_TAB_H)
	$(FLEX) -o $(LEXER_YY_C) $(LEXER_SRC)

# Windows targets
$(DLL_TARGET): $(PARSER_TAB_C) $(LEXER_YY_C)
	$(CC) $(CFLAGS) -shared -Iparser -Ilexer $(PARSER_TAB_C) $(LEXER_YY_C) -o $(DLL_TARGET)

$(EXE_TARGET): $(PARSER_TAB_C) $(LEXER_YY_C)
	$(CC) $(CFLAGS) -Iparser -Ilexer $(PARSER_TAB_C) $(LEXER_YY_C) -o $(EXE_TARGET)

# Linux targets
$(SO_TARGET): $(PARSER_TAB_C) $(LEXER_YY_C)
	$(CC) $(CFLAGS) -shared -fPIC -Iparser -Ilexer $(PARSER_TAB_C) $(LEXER_YY_C) -o $(SO_TARGET)

$(LINUX_EXE): $(PARSER_TAB_C) $(LEXER_YY_C)
	$(CC) $(CFLAGS) -Iparser -Ilexer $(PARSER_TAB_C) $(LEXER_YY_C) -o $(LINUX_EXE)
	chmod +x $(LINUX_EXE)

test: all
	python tests/run_tests.py
	python tests/test_gui_backend.py
	python tests/test_web_api.py

test-web:
	python tests/test_web_api.py

web:
	python backend/app.py

gui: all
	python gui/app.py

clean:
	rm -f $(PARSER_TAB_C) $(PARSER_TAB_H) $(PARSER_OUTPUT) $(LEXER_YY_C) $(DLL_TARGET) $(EXE_TARGET) $(SO_TARGET) $(LINUX_EXE)

help:
	@echo "Targets:"
	@echo "  all      - Build javacheck.dll and javacheck.exe (Windows)"
	@echo "  linux    - Build javacheck.so and javacheck (Linux / Docker)"
	@echo "  test     - Run full test suite (parser, GUI, and web API)"
	@echo "  test-web - Run Flask Web API tests"
	@echo "  web      - Launch Flask Web Application"
	@echo "  gui      - Launch Tkinter GUI application"
	@echo "  clean    - Remove generated parser, lexer, DLL, SO, and EXE files"
