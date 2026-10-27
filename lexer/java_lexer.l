%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "java_parser.tab.h"

int current_column = 1;

#define YY_USER_ACTION \
    yylloc.first_line = yylloc.last_line = yylineno; \
    yylloc.first_column = current_column; \
    yylloc.last_column = current_column + yyleng - 1; \
    current_column += yyleng;
%}

%option noyywrap
%option yylineno

/* Exclusive start conditions */
%x STATE_BLOCK_COMMENT
%x STATE_TEXT_BLOCK

/* Regular Expression Macros */
DIGIT           [0-9]
DIGITS          {DIGIT}([0-9_]*{DIGIT})?
HEX_DIGIT       [0-9a-fA-F]
HEX_DIGITS      {HEX_DIGIT}([0-9a-fA-F_]*{HEX_DIGIT})?
BIN_DIGIT       [01]
BIN_DIGITS      {BIN_DIGIT}([01_]*{BIN_DIGIT})?
OCT_DIGIT       [0-7]
OCT_DIGITS      {OCT_DIGIT}([0-7_]*{OCT_DIGIT})?

LETTER          [a-zA-Z_$]|[\x80-\xFF]
LETTER_OR_DIGIT [a-zA-Z0-9_$]|[\x80-\xFF]

EXPONENT        [eE][+-]?{DIGITS}
FLOAT_SUFFIX    [fFdD]
INT_SUFFIX      [lL]

ESCAPE_SEQ      \\[btnfr"'\\]|\\[0-3]?{OCT_DIGIT}{1,2}|\\u{HEX_DIGIT}{4}

%%

    /* =========================================================================
       Whitespace and Comments
       ========================================================================= */

[ \t\f\r]+                      { /* ignore whitespace */ }
\n                              { current_column = 1; }

"//"[^\r\n]*                    { /* single-line comment */ }

"/*"                            { BEGIN(STATE_BLOCK_COMMENT); }
<STATE_BLOCK_COMMENT>"*/"       { BEGIN(INITIAL); }
<STATE_BLOCK_COMMENT>\n         { current_column = 1; }
<STATE_BLOCK_COMMENT>.          { /* ignore */ }

    /* =========================================================================
       Keywords
       ========================================================================= */

"abstract"                      { return ABSTRACT; }
"assert"                        { return ASSERT; }
"boolean"                       { return BOOLEAN; }
"break"                         { return BREAK; }
"byte"                          { return BYTE; }
"case"                          { return CASE; }
"catch"                         { return CATCH; }
"char"                          { return CHAR; }
"class"                         { return CLASS; }
"const"                         { return CONST; }
"continue"                      { return CONTINUE; }
"default"                       { return DEFAULT; }
"do"                            { return DO; }
"double"                        { return DOUBLE; }
"else"                          { return ELSE; }
"enum"                          { return ENUM; }
"exports"                       { return EXPORTS; }
"extends"                       { return EXTENDS; }
"final"                         { return FINAL; }
"finally"                       { return FINALLY; }
"float"                         { return FLOAT; }
"for"                           { return FOR; }
"goto"                          { return GOTO; }
"if"                            { return IF; }
"implements"                    { return IMPLEMENTS; }
"import"                        { return IMPORT; }
"instanceof"                    { return INSTANCEOF; }
"int"                           { return INT; }
"interface"                     { return INTERFACE; }
"long"                          { return LONG; }
"module"                        { return MODULE; }
"native"                        { return NATIVE; }
"new"                           { return NEW; }
"non-sealed"                    { return NON_SEALED; }
"open"                          { return OPEN; }
"opens"                         { return OPENS; }
"package"                       { return PACKAGE; }
"permits"                       { return PERMITS; }
"private"                       { return PRIVATE; }
"protected"                     { return PROTECTED; }
"provides"                      { return PROVIDES; }
"public"                        { return PUBLIC; }
"record"                        { return RECORD; }
"requires"                      { return REQUIRES; }
"return"                        { return RETURN; }
"sealed"                        { return SEALED; }
"short"                         { return SHORT; }
"static"                        { return STATIC; }
"strictfp"                      { return STRICTFP; }
"super"                         { return SUPER; }
"switch"                        { return SWITCH; }
"synchronized"                  { return SYNCHRONIZED; }
"this"                          { return THIS; }
"throw"                         { return THROW; }
"throws"                        { return THROWS; }
"to"                            { return TO; }
"transient"                     { return TRANSIENT; }
"transitive"                    { return TRANSITIVE; }
"try"                           { return TRY; }
"uses"                          { return USES; }
"var"                           { return VAR; }
"void"                          { return VOID; }
"volatile"                      { return VOLATILE; }
"when"                          { return WHEN; }
"while"                         { return WHILE; }
"with"                          { return WITH; }
"yield"                         { return YIELD; }

    /* =========================================================================
       Literals
       ========================================================================= */

"true"                          { return BOOL_LITERAL; }
"false"                         { return BOOL_LITERAL; }
"null"                          { return NULL_LITERAL; }

    /* Binary Integers */
0[bB]{BIN_DIGITS}{INT_SUFFIX}?  { return BINARY_LITERAL; }

    /* Hexadecimal Integers */
0[xX]{HEX_DIGITS}{INT_SUFFIX}?  { return HEX_LITERAL; }

    /* Octal Integers */
0{OCT_DIGITS}{INT_SUFFIX}?      { return OCT_LITERAL; }

    /* Decimal Integers */
(0|[1-9]([0-9_]*[0-9])?){INT_SUFFIX}? { return DECIMAL_LITERAL; }

    /* Hexadecimal Floating Point */
0[xX]({HEX_DIGITS}?\.{HEX_DIGITS}|{HEX_DIGITS}\.?)[pP][+-]?{DIGITS}{FLOAT_SUFFIX}? { return HEX_FLOAT_LITERAL; }

    /* Decimal Floating Point */
{DIGITS}\.{DIGITS}?{EXPONENT}?{FLOAT_SUFFIX}?   { return FLOAT_LITERAL; }
\.{DIGITS}{EXPONENT}?{FLOAT_SUFFIX}?            { return FLOAT_LITERAL; }
{DIGITS}{EXPONENT}{FLOAT_SUFFIX}?               { return FLOAT_LITERAL; }
{DIGITS}{EXPONENT}?{FLOAT_SUFFIX}               { return FLOAT_LITERAL; }

    /* Character Literal */
'([^'\\\r\n]|{ESCAPE_SEQ})+'    { return CHAR_LITERAL; }

    /* Standard String Literal */
\"([^"\\\r\n]|{ESCAPE_SEQ})*\"  { return STRING_LITERAL; }

    /* Text Blocks */
"\"\"\""                        { BEGIN(STATE_TEXT_BLOCK); }
<STATE_TEXT_BLOCK>"\"\"\""      { BEGIN(INITIAL); return TEXT_BLOCK; }
<STATE_TEXT_BLOCK>\n            { current_column = 1; }
<STATE_TEXT_BLOCK>.             { /* ignore */ }

    /* =========================================================================
       Multi-Character Operators
       ========================================================================= */

">>>="                          { return URSHIFT_ASSIGN; }
">>="                           { return RSHIFT_ASSIGN; }
"<<="                           { return LSHIFT_ASSIGN; }
"+="                            { return ADD_ASSIGN; }
"-="                            { return SUB_ASSIGN; }
"*="                            { return MUL_ASSIGN; }
"/="                            { return DIV_ASSIGN; }
"&="                            { return AND_ASSIGN; }
"|="                            { return OR_ASSIGN; }
"^="                            { return XOR_ASSIGN; }
"%="                            { return MOD_ASSIGN; }

">>>"                           { return URSHIFT; }
">>"                            { return RSHIFT; }
"<<"                            { return LSHIFT; }

"=="                            { return EQUAL; }
"!="                            { return NOTEQUAL; }
"<="                            { return LE; }
">="                            { return GE; }

"&&"                            { return AND; }
"||"                            { return OR; }
"++"                            { return INC; }
"--"                            { return DEC; }

"->"                            { return ARROW; }
"::"                            { return COLONCOLON; }
"..."                           { return ELLIPSIS; }

    /* =========================================================================
       Single-Character Operators & Separators
       ========================================================================= */

"("                             { return LPAREN; }
")"                             { return RPAREN; }
"{"                             { return LBRACE; }
"}"                             { return RBRACE; }
"["[ \t\r\n]*"]"                {
    int col = yylloc.first_column;
    for (int i = 0; yytext[i]; i++) {
        if (yytext[i] == '\n') {
            col = 1;
        } else {
            col++;
        }
    }
    current_column = col;
    return LBRACK_RBRACK;
}
"["                             { return LBRACK; }
"]"                             { return RBRACK; }
";"                             { return SEMI; }
","                             { return COMMA; }
"."                             { return DOT; }
"="                             { return ASSIGN; }
">"                             { return GT; }
"<"                             { return LT; }
"!"                             { return BANG; }
"~"                             { return TILDE; }
"?"                             { return QUESTION; }
":"                             { return COLON; }
"+"                             { return ADD; }
"-"                             { return SUB; }
"*"                             { return MUL; }
"/"                             { return DIV; }
"&"                             { return BITAND; }
"|"                             { return BITOR; }
"^"                             { return CARET; }
"%"                             { return MOD; }
"@"                             { return AT; }

    /* =========================================================================
       Identifiers
       ========================================================================= */

{LETTER}{LETTER_OR_DIGIT}*      { return IDENTIFIER; }

    /* =========================================================================
       Fallback / Invalid character
       ========================================================================= */

.                               { return yytext[0]; }

%%
