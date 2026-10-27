/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_PARSER_JAVA_PARSER_TAB_H_INCLUDED
# define YY_YY_PARSER_JAVA_PARSER_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    ABSTRACT = 258,                /* ABSTRACT  */
    ASSERT = 259,                  /* ASSERT  */
    BOOLEAN = 260,                 /* BOOLEAN  */
    BREAK = 261,                   /* BREAK  */
    BYTE = 262,                    /* BYTE  */
    CASE = 263,                    /* CASE  */
    CATCH = 264,                   /* CATCH  */
    CHAR = 265,                    /* CHAR  */
    CLASS = 266,                   /* CLASS  */
    CONST = 267,                   /* CONST  */
    CONTINUE = 268,                /* CONTINUE  */
    DEFAULT = 269,                 /* DEFAULT  */
    DO = 270,                      /* DO  */
    DOUBLE = 271,                  /* DOUBLE  */
    ELSE = 272,                    /* ELSE  */
    ENUM = 273,                    /* ENUM  */
    EXPORTS = 274,                 /* EXPORTS  */
    EXTENDS = 275,                 /* EXTENDS  */
    FINAL = 276,                   /* FINAL  */
    FINALLY = 277,                 /* FINALLY  */
    FLOAT = 278,                   /* FLOAT  */
    FOR = 279,                     /* FOR  */
    GOTO = 280,                    /* GOTO  */
    IF = 281,                      /* IF  */
    IMPLEMENTS = 282,              /* IMPLEMENTS  */
    IMPORT = 283,                  /* IMPORT  */
    INSTANCEOF = 284,              /* INSTANCEOF  */
    INT = 285,                     /* INT  */
    INTERFACE = 286,               /* INTERFACE  */
    LONG = 287,                    /* LONG  */
    MODULE = 288,                  /* MODULE  */
    NATIVE = 289,                  /* NATIVE  */
    NEW = 290,                     /* NEW  */
    NON_SEALED = 291,              /* NON_SEALED  */
    OPEN = 292,                    /* OPEN  */
    OPENS = 293,                   /* OPENS  */
    PACKAGE = 294,                 /* PACKAGE  */
    PERMITS = 295,                 /* PERMITS  */
    PRIVATE = 296,                 /* PRIVATE  */
    PROTECTED = 297,               /* PROTECTED  */
    PROVIDES = 298,                /* PROVIDES  */
    PUBLIC = 299,                  /* PUBLIC  */
    RECORD = 300,                  /* RECORD  */
    REQUIRES = 301,                /* REQUIRES  */
    RETURN = 302,                  /* RETURN  */
    SEALED = 303,                  /* SEALED  */
    SHORT = 304,                   /* SHORT  */
    STATIC = 305,                  /* STATIC  */
    STRICTFP = 306,                /* STRICTFP  */
    SUPER = 307,                   /* SUPER  */
    SWITCH = 308,                  /* SWITCH  */
    SYNCHRONIZED = 309,            /* SYNCHRONIZED  */
    THIS = 310,                    /* THIS  */
    THROW = 311,                   /* THROW  */
    THROWS = 312,                  /* THROWS  */
    TO = 313,                      /* TO  */
    TRANSIENT = 314,               /* TRANSIENT  */
    TRANSITIVE = 315,              /* TRANSITIVE  */
    TRY = 316,                     /* TRY  */
    USES = 317,                    /* USES  */
    VAR = 318,                     /* VAR  */
    VOID = 319,                    /* VOID  */
    VOLATILE = 320,                /* VOLATILE  */
    WHEN = 321,                    /* WHEN  */
    WHILE = 322,                   /* WHILE  */
    WITH = 323,                    /* WITH  */
    YIELD = 324,                   /* YIELD  */
    DECIMAL_LITERAL = 325,         /* DECIMAL_LITERAL  */
    HEX_LITERAL = 326,             /* HEX_LITERAL  */
    OCT_LITERAL = 327,             /* OCT_LITERAL  */
    BINARY_LITERAL = 328,          /* BINARY_LITERAL  */
    FLOAT_LITERAL = 329,           /* FLOAT_LITERAL  */
    HEX_FLOAT_LITERAL = 330,       /* HEX_FLOAT_LITERAL  */
    BOOL_LITERAL = 331,            /* BOOL_LITERAL  */
    CHAR_LITERAL = 332,            /* CHAR_LITERAL  */
    STRING_LITERAL = 333,          /* STRING_LITERAL  */
    TEXT_BLOCK = 334,              /* TEXT_BLOCK  */
    NULL_LITERAL = 335,            /* NULL_LITERAL  */
    IDENTIFIER = 336,              /* IDENTIFIER  */
    LPAREN = 337,                  /* LPAREN  */
    RPAREN = 338,                  /* RPAREN  */
    LBRACE = 339,                  /* LBRACE  */
    RBRACE = 340,                  /* RBRACE  */
    LBRACK = 341,                  /* LBRACK  */
    RBRACK = 342,                  /* RBRACK  */
    LBRACK_RBRACK = 343,           /* LBRACK_RBRACK  */
    SEMI = 344,                    /* SEMI  */
    COMMA = 345,                   /* COMMA  */
    DOT = 346,                     /* DOT  */
    ELLIPSIS = 347,                /* ELLIPSIS  */
    AT = 348,                      /* AT  */
    COLONCOLON = 349,              /* COLONCOLON  */
    ASSIGN = 350,                  /* ASSIGN  */
    GT = 351,                      /* GT  */
    LT = 352,                      /* LT  */
    BANG = 353,                    /* BANG  */
    TILDE = 354,                   /* TILDE  */
    QUESTION = 355,                /* QUESTION  */
    COLON = 356,                   /* COLON  */
    EQUAL = 357,                   /* EQUAL  */
    LE = 358,                      /* LE  */
    GE = 359,                      /* GE  */
    NOTEQUAL = 360,                /* NOTEQUAL  */
    AND = 361,                     /* AND  */
    OR = 362,                      /* OR  */
    INC = 363,                     /* INC  */
    DEC = 364,                     /* DEC  */
    ADD = 365,                     /* ADD  */
    SUB = 366,                     /* SUB  */
    MUL = 367,                     /* MUL  */
    DIV = 368,                     /* DIV  */
    BITAND = 369,                  /* BITAND  */
    BITOR = 370,                   /* BITOR  */
    CARET = 371,                   /* CARET  */
    MOD = 372,                     /* MOD  */
    LSHIFT = 373,                  /* LSHIFT  */
    RSHIFT = 374,                  /* RSHIFT  */
    URSHIFT = 375,                 /* URSHIFT  */
    ADD_ASSIGN = 376,              /* ADD_ASSIGN  */
    SUB_ASSIGN = 377,              /* SUB_ASSIGN  */
    MUL_ASSIGN = 378,              /* MUL_ASSIGN  */
    DIV_ASSIGN = 379,              /* DIV_ASSIGN  */
    AND_ASSIGN = 380,              /* AND_ASSIGN  */
    OR_ASSIGN = 381,               /* OR_ASSIGN  */
    XOR_ASSIGN = 382,              /* XOR_ASSIGN  */
    MOD_ASSIGN = 383,              /* MOD_ASSIGN  */
    LSHIFT_ASSIGN = 384,           /* LSHIFT_ASSIGN  */
    RSHIFT_ASSIGN = 385,           /* RSHIFT_ASSIGN  */
    URSHIFT_ASSIGN = 386,          /* URSHIFT_ASSIGN  */
    ARROW = 387,                   /* ARROW  */
    LOWER_THAN_ELSE = 388,         /* LOWER_THAN_ELSE  */
    UNARY = 389,                   /* UNARY  */
    PREFIX_OP = 390,               /* PREFIX_OP  */
    POSTFIX_OP = 391               /* POSTFIX_OP  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif

/* Location type.  */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE YYLTYPE;
struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
};
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif


extern YYSTYPE yylval;
extern YYLTYPE yylloc;

int yyparse (void);


#endif /* !YY_YY_PARSER_JAVA_PARSER_TAB_H_INCLUDED  */
