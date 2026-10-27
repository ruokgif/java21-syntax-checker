#ifndef JAVA_TOKENS_H
#define JAVA_TOKENS_H

/* Token codes matching the Java grammar specification */
typedef enum {
    TOK_EOF = 0,

    /* Keywords */
    TOK_ABSTRACT = 258,
    TOK_ASSERT,
    TOK_BOOLEAN,
    TOK_BREAK,
    TOK_BYTE,
    TOK_CASE,
    TOK_CATCH,
    TOK_CHAR,
    TOK_CLASS,
    TOK_CONST,
    TOK_CONTINUE,
    TOK_DEFAULT,
    TOK_DO,
    TOK_DOUBLE,
    TOK_ELSE,
    TOK_ENUM,
    TOK_EXPORTS,
    TOK_EXTENDS,
    TOK_FINAL,
    TOK_FINALLY,
    TOK_FLOAT,
    TOK_FOR,
    TOK_GOTO,
    TOK_IF,
    TOK_IMPLEMENTS,
    TOK_IMPORT,
    TOK_INSTANCEOF,
    TOK_INT,
    TOK_INTERFACE,
    TOK_LONG,
    TOK_MODULE,
    TOK_NATIVE,
    TOK_NEW,
    TOK_NON_SEALED,
    TOK_OPEN,
    TOK_OPENS,
    TOK_PACKAGE,
    TOK_PERMITS,
    TOK_PRIVATE,
    TOK_PROTECTED,
    TOK_PROVIDES,
    TOK_PUBLIC,
    TOK_RECORD,
    TOK_REQUIRES,
    TOK_RETURN,
    TOK_SEALED,
    TOK_SHORT,
    TOK_STATIC,
    TOK_STRICTFP,
    TOK_SUPER,
    TOK_SWITCH,
    TOK_SYNCHRONIZED,
    TOK_THIS,
    TOK_THROW,
    TOK_THROWS,
    TOK_TO,
    TOK_TRANSIENT,
    TOK_TRANSITIVE,
    TOK_TRY,
    TOK_USES,
    TOK_VAR,
    TOK_VOID,
    TOK_VOLATILE,
    TOK_WHEN,
    TOK_WHILE,
    TOK_WITH,
    TOK_YIELD,

    /* Literals */
    TOK_DECIMAL_LITERAL,
    TOK_HEX_LITERAL,
    TOK_OCT_LITERAL,
    TOK_BINARY_LITERAL,
    TOK_FLOAT_LITERAL,
    TOK_HEX_FLOAT_LITERAL,
    TOK_BOOL_LITERAL,
    TOK_CHAR_LITERAL,
    TOK_STRING_LITERAL,
    TOK_TEXT_BLOCK,
    TOK_NULL_LITERAL,

    /* Identifiers */
    TOK_IDENTIFIER,

    /* Separators */
    TOK_LPAREN,     /* ( */
    TOK_RPAREN,     /* ) */
    TOK_LBRACE,     /* { */
    TOK_RBRACE,     /* } */
    TOK_LBRACK,     /* [ */
    TOK_RBRACK,     /* ] */
    TOK_LBRACK_RBRACK, /* [] */
    TOK_SEMI,       /* ; */
    TOK_COMMA,      /* , */
    TOK_DOT,        /* . */
    TOK_ELLIPSIS,   /* ... */
    TOK_AT,         /* @ */
    TOK_COLONCOLON, /* :: */

    /* Operators */
    TOK_ASSIGN,         /* = */
    TOK_GT,             /* > */
    TOK_LT,             /* < */
    TOK_BANG,           /* ! */
    TOK_TILDE,          /* ~ */
    TOK_QUESTION,       /* ? */
    TOK_COLON,          /* : */
    TOK_EQUAL,          /* == */
    TOK_LE,             /* <= */
    TOK_GE,             /* >= */
    TOK_NOTEQUAL,       /* != */
    TOK_AND,            /* && */
    TOK_OR,             /* || */
    TOK_INC,            /* ++ */
    TOK_DEC,            /* -- */
    TOK_ADD,            /* + */
    TOK_SUB,            /* - */
    TOK_MUL,            /* * */
    TOK_DIV,            /* / */
    TOK_BITAND,         /* & */
    TOK_BITOR,          /* | */
    TOK_CARET,          /* ^ */
    TOK_MOD,            /* % */
    TOK_LSHIFT,         /* << */
    TOK_RSHIFT,         /* >> */
    TOK_URSHIFT,        /* >>> */
    TOK_ADD_ASSIGN,     /* += */
    TOK_SUB_ASSIGN,     /* -= */
    TOK_MUL_ASSIGN,     /* *= */
    TOK_DIV_ASSIGN,     /* /= */
    TOK_AND_ASSIGN,     /* &= */
    TOK_OR_ASSIGN,      /* |= */
    TOK_XOR_ASSIGN,     /* ^= */
    TOK_MOD_ASSIGN,     /* %= */
    TOK_LSHIFT_ASSIGN,  /* <<= */
    TOK_RSHIFT_ASSIGN,  /* >>= */
    TOK_URSHIFT_ASSIGN, /* >>>= */
    TOK_ARROW           /* -> */
} JavaToken;

const char *token_to_string(int token);

#endif /* JAVA_TOKENS_H */
