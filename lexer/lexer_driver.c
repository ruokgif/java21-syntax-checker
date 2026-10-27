#include <stdio.h>
#include <stdlib.h>
#include "tokens.h"

extern int yylex(void);
extern int yylineno;
extern char *yytext;
extern FILE *yyin;

const char *token_to_string(int token) {
    switch (token) {
        case TOK_EOF: return "EOF";
        case TOK_ABSTRACT: return "ABSTRACT";
        case TOK_ASSERT: return "ASSERT";
        case TOK_BOOLEAN: return "BOOLEAN";
        case TOK_BREAK: return "BREAK";
        case TOK_BYTE: return "BYTE";
        case TOK_CASE: return "CASE";
        case TOK_CATCH: return "CATCH";
        case TOK_CHAR: return "CHAR";
        case TOK_CLASS: return "CLASS";
        case TOK_CONST: return "CONST";
        case TOK_CONTINUE: return "CONTINUE";
        case TOK_DEFAULT: return "DEFAULT";
        case TOK_DO: return "DO";
        case TOK_DOUBLE: return "DOUBLE";
        case TOK_ELSE: return "ELSE";
        case TOK_ENUM: return "ENUM";
        case TOK_EXPORTS: return "EXPORTS";
        case TOK_EXTENDS: return "EXTENDS";
        case TOK_FINAL: return "FINAL";
        case TOK_FINALLY: return "FINALLY";
        case TOK_FLOAT: return "FLOAT";
        case TOK_FOR: return "FOR";
        case TOK_GOTO: return "GOTO";
        case TOK_IF: return "IF";
        case TOK_IMPLEMENTS: return "IMPLEMENTS";
        case TOK_IMPORT: return "IMPORT";
        case TOK_INSTANCEOF: return "INSTANCEOF";
        case TOK_INT: return "INT";
        case TOK_INTERFACE: return "INTERFACE";
        case TOK_LONG: return "LONG";
        case TOK_MODULE: return "MODULE";
        case TOK_NATIVE: return "NATIVE";
        case TOK_NEW: return "NEW";
        case TOK_NON_SEALED: return "NON_SEALED";
        case TOK_OPEN: return "OPEN";
        case TOK_OPENS: return "OPENS";
        case TOK_PACKAGE: return "PACKAGE";
        case TOK_PERMITS: return "PERMITS";
        case TOK_PRIVATE: return "PRIVATE";
        case TOK_PROTECTED: return "PROTECTED";
        case TOK_PROVIDES: return "PROVIDES";
        case TOK_PUBLIC: return "PUBLIC";
        case TOK_RECORD: return "RECORD";
        case TOK_REQUIRES: return "REQUIRES";
        case TOK_RETURN: return "RETURN";
        case TOK_SEALED: return "SEALED";
        case TOK_SHORT: return "SHORT";
        case TOK_STATIC: return "STATIC";
        case TOK_STRICTFP: return "STRICTFP";
        case TOK_SUPER: return "SUPER";
        case TOK_SWITCH: return "SWITCH";
        case TOK_SYNCHRONIZED: return "SYNCHRONIZED";
        case TOK_THIS: return "THIS";
        case TOK_THROW: return "THROW";
        case TOK_THROWS: return "THROWS";
        case TOK_TO: return "TO";
        case TOK_TRANSIENT: return "TRANSIENT";
        case TOK_TRANSITIVE: return "TRANSITIVE";
        case TOK_TRY: return "TRY";
        case TOK_USES: return "USES";
        case TOK_VAR: return "VAR";
        case TOK_VOID: return "VOID";
        case TOK_VOLATILE: return "VOLATILE";
        case TOK_WHEN: return "WHEN";
        case TOK_WHILE: return "WHILE";
        case TOK_WITH: return "WITH";
        case TOK_YIELD: return "YIELD";

        case TOK_DECIMAL_LITERAL: return "DECIMAL_LITERAL";
        case TOK_HEX_LITERAL: return "HEX_LITERAL";
        case TOK_OCT_LITERAL: return "OCT_LITERAL";
        case TOK_BINARY_LITERAL: return "BINARY_LITERAL";
        case TOK_FLOAT_LITERAL: return "FLOAT_LITERAL";
        case TOK_HEX_FLOAT_LITERAL: return "HEX_FLOAT_LITERAL";
        case TOK_BOOL_LITERAL: return "BOOL_LITERAL";
        case TOK_CHAR_LITERAL: return "CHAR_LITERAL";
        case TOK_STRING_LITERAL: return "STRING_LITERAL";
        case TOK_TEXT_BLOCK: return "TEXT_BLOCK";
        case TOK_NULL_LITERAL: return "NULL_LITERAL";

        case TOK_IDENTIFIER: return "IDENTIFIER";

        case TOK_LPAREN: return "LPAREN '('";
        case TOK_RPAREN: return "RPAREN ')'";
        case TOK_LBRACE: return "LBRACE '{'";
        case TOK_RBRACE: return "RBRACE '}'";
        case TOK_LBRACK: return "LBRACK '['";
        case TOK_RBRACK: return "RBRACK ']'";
        case TOK_LBRACK_RBRACK: return "LBRACK_RBRACK '[]'";
        case TOK_SEMI: return "SEMI ';'";
        case TOK_COMMA: return "COMMA ','";
        case TOK_DOT: return "DOT '.'";
        case TOK_ELLIPSIS: return "ELLIPSIS '...'";
        case TOK_AT: return "AT '@'";
        case TOK_COLONCOLON: return "COLONCOLON '::'";

        case TOK_ASSIGN: return "ASSIGN '='";
        case TOK_GT: return "GT '>'";
        case TOK_LT: return "LT '<'";
        case TOK_BANG: return "BANG '!'";
        case TOK_TILDE: return "TILDE '~'";
        case TOK_QUESTION: return "QUESTION '?'";
        case TOK_COLON: return "COLON ':'";
        case TOK_EQUAL: return "EQUAL '=='";
        case TOK_LE: return "LE '<='";
        case TOK_GE: return "GE '>='";
        case TOK_NOTEQUAL: return "NOTEQUAL '!='";
        case TOK_AND: return "AND '&&'";
        case TOK_OR: return "OR '||'";
        case TOK_INC: return "INC '++'";
        case TOK_DEC: return "DEC '--'";
        case TOK_ADD: return "ADD '+'";
        case TOK_SUB: return "SUB '-'";
        case TOK_MUL: return "MUL '*'";
        case TOK_DIV: return "DIV '/'";
        case TOK_BITAND: return "BITAND '&'";
        case TOK_BITOR: return "BITOR '|'";
        case TOK_CARET: return "CARET '^'";
        case TOK_MOD: return "MOD '%'";
        case TOK_LSHIFT: return "LSHIFT '<<'";
        case TOK_RSHIFT: return "RSHIFT '>>'";
        case TOK_URSHIFT: return "URSHIFT '>>>'";
        case TOK_ADD_ASSIGN: return "ADD_ASSIGN '+='";
        case TOK_SUB_ASSIGN: return "SUB_ASSIGN '-='";
        case TOK_MUL_ASSIGN: return "MUL_ASSIGN '*='";
        case TOK_DIV_ASSIGN: return "DIV_ASSIGN '/='";
        case TOK_AND_ASSIGN: return "AND_ASSIGN '&='";
        case TOK_OR_ASSIGN: return "OR_ASSIGN '|='";
        case TOK_XOR_ASSIGN: return "XOR_ASSIGN '^='";
        case TOK_MOD_ASSIGN: return "MOD_ASSIGN '%='";
        case TOK_LSHIFT_ASSIGN: return "LSHIFT_ASSIGN '<<='";
        case TOK_RSHIFT_ASSIGN: return "RSHIFT_ASSIGN '>>='";
        case TOK_URSHIFT_ASSIGN: return "URSHIFT_ASSIGN '>>>='";
        case TOK_ARROW: return "ARROW '->'";
        default: {
            static char buf[32];
            snprintf(buf, sizeof(buf), "CHAR_TOKEN('%c' / %d)", (char)token, token);
            return buf;
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        FILE *f = fopen(argv[1], "r");
        if (!f) {
            fprintf(stderr, "Error: Could not open file %s\n", argv[1]);
            return 1;
        }
        yyin = f;
    } else {
        yyin = stdin;
    }

    int token;
    while ((token = yylex()) != 0) {
        printf("Line %4d | %-22s | Text: '%s'\n", yylineno, token_to_string(token), yytext);
    }
    printf("Line %4d | %-22s | [End of File]\n", yylineno, token_to_string(0));

    if (argc > 1 && yyin) {
        fclose(yyin);
    }
    return 0;
}
