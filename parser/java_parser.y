%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex(void);
extern int yylineno;
extern int current_column;
extern char *yytext;
extern FILE *yyin;
extern void yyrestart(FILE *input_file);

void yyerror(const char *s);
int syntax_error_occurred = 0;
int error_line = 0;
%}

%define parse.error verbose
%locations

/* =========================================================================
   Token Declarations
   ========================================================================= */

/* Keywords */
%token ABSTRACT ASSERT BOOLEAN BREAK BYTE CASE CATCH CHAR CLASS CONST CONTINUE
%token DEFAULT DO DOUBLE ELSE ENUM EXPORTS EXTENDS FINAL FINALLY FLOAT FOR GOTO
%token IF IMPLEMENTS IMPORT INSTANCEOF INT INTERFACE LONG MODULE NATIVE NEW
%token NON_SEALED OPEN OPENS PACKAGE PERMITS PRIVATE PROTECTED PROVIDES PUBLIC
%token RECORD REQUIRES RETURN SEALED SHORT STATIC STRICTFP SUPER SWITCH
%token SYNCHRONIZED THIS THROW THROWS TO TRANSIENT TRANSITIVE TRY USES VAR
%token VOID VOLATILE WHEN WHILE WITH YIELD

/* Literals */
%token DECIMAL_LITERAL HEX_LITERAL OCT_LITERAL BINARY_LITERAL
%token FLOAT_LITERAL HEX_FLOAT_LITERAL BOOL_LITERAL CHAR_LITERAL
%token STRING_LITERAL TEXT_BLOCK NULL_LITERAL

/* Identifier */
%token IDENTIFIER

/* Separators */
%token LPAREN RPAREN LBRACE RBRACE LBRACK RBRACK LBRACK_RBRACK SEMI COMMA DOT ELLIPSIS AT COLONCOLON

/* Operators */
%token ASSIGN GT LT BANG TILDE QUESTION COLON EQUAL LE GE NOTEQUAL
%token AND OR INC DEC ADD SUB MUL DIV BITAND BITOR CARET MOD
%token LSHIFT RSHIFT URSHIFT
%token ADD_ASSIGN SUB_ASSIGN MUL_ASSIGN DIV_ASSIGN AND_ASSIGN OR_ASSIGN XOR_ASSIGN
%token MOD_ASSIGN LSHIFT_ASSIGN RSHIFT_ASSIGN URSHIFT_ASSIGN ARROW

/* =========================================================================
   Operator Precedence & Associativity
   ========================================================================= */

%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%right ARROW
%right ASSIGN ADD_ASSIGN SUB_ASSIGN MUL_ASSIGN DIV_ASSIGN AND_ASSIGN OR_ASSIGN XOR_ASSIGN MOD_ASSIGN LSHIFT_ASSIGN RSHIFT_ASSIGN URSHIFT_ASSIGN
%right QUESTION COLON
%left OR
%left AND
%left BITOR
%left CARET
%left BITAND
%left EQUAL NOTEQUAL
%left LT GT LE GE INSTANCEOF
%left LSHIFT RSHIFT URSHIFT
%left ADD SUB
%left MUL DIV MOD
%right UNARY PREFIX_OP
%left POSTFIX_OP

%start compilationUnit

%%

/* =========================================================================
   1. COMPILATION UNIT & PACKAGES & IMPORTS
   ========================================================================= */

compilationUnit
    : packageDeclaration topLevelDeclarations
    | topLevelDeclarations
    | moduleDeclaration
    ;

packageDeclaration
    : annotations_opt PACKAGE qualifiedName SEMI
    ;

topLevelDeclarations
    : /* empty */
    | topLevelDeclarations topLevelDeclaration
    ;

topLevelDeclaration
    : importDeclaration
    | typeDeclaration
    ;

importDeclaration
    : IMPORT STATIC qualifiedName SEMI
    | IMPORT STATIC qualifiedName DOT MUL SEMI
    | IMPORT qualifiedName SEMI
    | IMPORT qualifiedName DOT MUL SEMI
    ;

typeDeclaration
    : modifiers_opt classDeclaration
    | modifiers_opt enumDeclaration
    | modifiers_opt interfaceDeclaration
    | modifiers_opt annotationTypeDeclaration
    | modifiers_opt recordDeclaration
    ;

/* =========================================================================
   2. MODULES (Java 9+)
   ========================================================================= */

moduleDeclaration
    : annotations_opt open_opt MODULE qualifiedName LBRACE moduleDirectives RBRACE
    ;

open_opt
    : /* empty */
    | OPEN
    ;

moduleDirectives
    : /* empty */
    | moduleDirectives moduleDirective
    ;

moduleDirective
    : REQUIRES requiresModifiers_opt qualifiedName SEMI
    | EXPORTS qualifiedName exportsTo_opt SEMI
    | OPENS qualifiedName exportsTo_opt SEMI
    | USES qualifiedName SEMI
    | PROVIDES qualifiedName WITH qualifiedNameList SEMI
    ;

requiresModifiers_opt
    : /* empty */
    | requiresModifiers_opt TRANSITIVE
    | requiresModifiers_opt STATIC
    ;

exportsTo_opt
    : /* empty */
    | TO qualifiedNameList
    ;

/* =========================================================================
   3. MODIFIERS & ANNOTATIONS
   ========================================================================= */

modifiers_opt
    : /* empty */
    | modifiers_opt modifier
    ;

modifier
    : annotation
    | PUBLIC
    | PROTECTED
    | PRIVATE
    | STATIC
    | ABSTRACT
    | FINAL
    | STRICTFP
    | SEALED
    | NON_SEALED
    | NATIVE
    | SYNCHRONIZED
    | TRANSIENT
    | VOLATILE
    | DEFAULT
    ;

variableModifiers_opt
    : /* empty */
    | variableModifiers
    ;

variableModifiers
    : variableModifier
    | variableModifiers variableModifier
    ;

variableModifier
    : FINAL
    | annotation
    ;

annotations_opt
    : /* empty */
    | annotations_opt annotation
    ;

annotation
    : AT qualifiedName
    | AT qualifiedName LPAREN elementValuePairs_opt RPAREN
    | AT qualifiedName LPAREN elementValue RPAREN
    ;

elementValuePairs_opt
    : /* empty */
    | elementValuePairs
    ;

elementValuePairs
    : elementValuePair
    | elementValuePairs COMMA elementValuePair
    ;

elementValuePair
    : identifier ASSIGN elementValue
    ;

elementValue
    : expression
    | annotation
    | elementValueArrayInitializer
    ;

elementValueArrayInitializer
    : LBRACE elementValues_opt RBRACE
    ;

elementValues_opt
    : /* empty */
    | elementValueList
    | elementValueList COMMA
    ;

elementValueList
    : elementValue
    | elementValueList COMMA elementValue
    ;

comma_opt
    : /* empty */
    | COMMA
    ;

/* =========================================================================
   4. CLASS, INTERFACE, ENUM, RECORD DECLARATIONS
   ========================================================================= */

classDeclaration
    : CLASS identifier typeParameters_opt extendsClause_opt implementsClause_opt permitsClause_opt classBody
    ;

extendsClause_opt
    : /* empty */
    | EXTENDS typeType
    ;

implementsClause_opt
    : /* empty */
    | IMPLEMENTS typeList
    ;

permitsClause_opt
    : /* empty */
    | PERMITS typeList
    ;

classBody
    : LBRACE classBodyDeclarations RBRACE
    ;

classBodyDeclarations
    : /* empty */
    | classBodyDeclarations classBodyDeclaration
    ;

classBodyDeclaration
    : STATIC block
    | block
    | modifiers_opt memberDeclaration
    ;

memberDeclaration
    : methodDeclaration
    | genericMethodDeclaration
    | fieldDeclaration
    | constructorDeclaration
    | genericConstructorDeclaration
    | compactConstructorDeclaration
    | classDeclaration
    | enumDeclaration
    | interfaceDeclaration
    | annotationTypeDeclaration
    | recordDeclaration
    ;

/* Record Declaration (Java 14+) */
recordDeclaration
    : RECORD identifier typeParameters_opt recordHeader implementsClause_opt recordBody
    ;

recordHeader
    : LPAREN recordComponentList_opt RPAREN
    ;

recordComponentList_opt
    : /* empty */
    | recordComponentList
    ;

recordComponentList
    : recordComponent
    | recordComponentList COMMA recordComponent
    ;

recordComponent
    : variableModifiers_opt typeType identifier
    | variableModifiers_opt typeType ELLIPSIS identifier
    ;

recordBody
    : LBRACE recordBodyDeclarations RBRACE
    ;

recordBodyDeclarations
    : /* empty */
    | recordBodyDeclarations recordBodyDeclaration
    ;

recordBodyDeclaration
    : classBodyDeclaration
    | compactConstructorDeclaration
    ;

compactConstructorDeclaration
    : identifier block
    ;

/* Interface Declaration */
interfaceDeclaration
    : INTERFACE identifier typeParameters_opt interfaceExtends_opt permitsClause_opt interfaceBody
    ;

interfaceExtends_opt
    : /* empty */
    | EXTENDS typeList
    ;

interfaceBody
    : LBRACE interfaceBodyDeclarations RBRACE
    ;

interfaceBodyDeclarations
    : /* empty */
    | interfaceBodyDeclarations interfaceBodyDeclaration
    ;

interfaceBodyDeclaration
    : modifiers_opt interfaceMemberDeclaration
    ;

interfaceMemberDeclaration
    : constDeclaration
    | interfaceMethodDeclaration
    | genericInterfaceMethodDeclaration
    | classDeclaration
    | enumDeclaration
    | interfaceDeclaration
    | annotationTypeDeclaration
    | recordDeclaration
    ;

constDeclaration
    : typeType constantDeclaratorList SEMI
    ;

constantDeclaratorList
    : constantDeclarator
    | constantDeclaratorList COMMA constantDeclarator
    ;

constantDeclarator
    : identifier dims_opt ASSIGN variableInitializer
    ;

interfaceMethodDeclaration
    : typeType identifier formalParameters dims_opt throwsClause_opt methodBody
    | VOID identifier formalParameters dims_opt throwsClause_opt methodBody
    ;

genericInterfaceMethodDeclaration
    : typeParameters typeType identifier formalParameters dims_opt throwsClause_opt methodBody
    | typeParameters VOID identifier formalParameters dims_opt throwsClause_opt methodBody
    ;

/* Enum Declaration */
enumDeclaration
    : ENUM identifier implementsClause_opt LBRACE enumConstants_opt comma_opt enumBodyDeclarations_opt RBRACE
    ;

enumConstants_opt
    : /* empty */
    | enumConstantList
    ;

enumConstantList
    : enumConstant
    | enumConstantList COMMA enumConstant
    ;

enumConstant
    : annotations_opt identifier arguments_opt classBody_opt
    ;

classBody_opt
    : /* empty */
    | classBody
    ;

enumBodyDeclarations_opt
    : /* empty */
    | SEMI classBodyDeclarations
    ;

/* Annotation Type Declaration */
annotationTypeDeclaration
    : AT INTERFACE identifier annotationTypeBody
    ;

annotationTypeBody
    : LBRACE annotationTypeElementDeclarations RBRACE
    ;

annotationTypeElementDeclarations
    : /* empty */
    | annotationTypeElementDeclarations annotationTypeElementDeclaration
    ;

annotationTypeElementDeclaration
    : modifiers_opt annotationTypeElementRest
    ;

annotationTypeElementRest
    : typeType identifier LPAREN RPAREN defaultValue_opt SEMI
    | typeType variableDeclarators SEMI
    | classDeclaration
    | enumDeclaration
    | interfaceDeclaration
    | annotationTypeDeclaration
    | recordDeclaration
    ;

defaultValue_opt
    : /* empty */
    | DEFAULT elementValue
    ;

/* =========================================================================
   5. MEMBERS: FIELDS, METHODS, CONSTRUCTORS
   ========================================================================= */

fieldDeclaration
    : typeType variableDeclarators SEMI
    ;

variableDeclarators
    : variableDeclarator
    | variableDeclarators COMMA variableDeclarator
    ;

variableDeclarator
    : variableDeclaratorId
    | variableDeclaratorId ASSIGN variableInitializer
    ;

variableDeclaratorId
    : identifier dims_opt
    ;

variableInitializer
    : arrayInitializer
    | expression
    ;

arrayInitializer
    : LBRACE variableInitializers_opt RBRACE
    ;

variableInitializers_opt
    : /* empty */
    | variableInitializerList
    | variableInitializerList COMMA
    ;

variableInitializerList
    : variableInitializer
    | variableInitializerList COMMA variableInitializer
    ;

methodDeclaration
    : typeType identifier formalParameters dims_opt throwsClause_opt methodBody
    | VOID identifier formalParameters dims_opt throwsClause_opt methodBody
    ;

genericMethodDeclaration
    : typeParameters typeType identifier formalParameters dims_opt throwsClause_opt methodBody
    | typeParameters VOID identifier formalParameters dims_opt throwsClause_opt methodBody
    ;

constructorDeclaration
    : identifier formalParameters throwsClause_opt block
    ;

genericConstructorDeclaration
    : typeParameters identifier formalParameters throwsClause_opt block
    ;

methodBody
    : block
    | SEMI
    ;

throwsClause_opt
    : /* empty */
    | THROWS qualifiedNameList
    ;

formalParameters
    : LPAREN formalParameterList_opt RPAREN
    ;

formalParameterList_opt
    : /* empty */
    | formalParameterList
    ;

formalParameterList
    : formalParameter
    | formalParameterList COMMA formalParameter
    | lastFormalParameter
    | formalParameterList COMMA lastFormalParameter
    ;

formalParameter
    : typeType variableDeclaratorId
    | variableModifiers typeType variableDeclaratorId
    ;

lastFormalParameter
    : typeType annotations_opt ELLIPSIS variableDeclaratorId
    | variableModifiers typeType annotations_opt ELLIPSIS variableDeclaratorId
    ;

/* =========================================================================
   6. TYPES & GENERICS
   ========================================================================= */

typeList
    : typeType
    | typeList COMMA typeType
    ;

typeType
    : primitiveType dims_opt
    | classOrInterfaceType dims_opt
    | annotation typeType
    ;

primitiveType
    : BOOLEAN
    | CHAR
    | BYTE
    | SHORT
    | INT
    | LONG
    | FLOAT
    | DOUBLE
    ;

primary
    : qualifiedName
    | LPAREN expression RPAREN
    | THIS
    | SUPER
    | literal
    | qualifiedName dims_opt DOT CLASS
    | primitiveType dims_opt DOT CLASS
    | VOID DOT CLASS
    | NEW creator
    | SWITCH LPAREN expression RPAREN switchBlock
    ;

classOrInterfaceType
    : qualifiedName
    | qualifiedName typeArguments
    ;

typeArguments_opt
    : /* empty */
    | typeArguments
    ;

typeArguments
    : LT typeArgumentList GT
    ;

typeArgumentList
    : typeArgument
    | typeArgumentList COMMA typeArgument
    ;

typeArgument
    : typeType
    | QUESTION
    | QUESTION EXTENDS typeType
    | QUESTION SUPER typeType
    ;

typeParameters_opt
    : /* empty */
    | typeParameters
    ;

typeParameters
    : LT typeParameterList GT
    ;

typeParameterList
    : typeParameter
    | typeParameterList COMMA typeParameter
    ;

typeParameter
    : annotations_opt identifier typeBound_opt
    ;

typeBound_opt
    : /* empty */
    | EXTENDS typeBoundList
    ;

typeBoundList
    : typeType
    | typeBoundList BITAND typeType
    ;

dims_opt
    : /* empty */
    | dims_opt LBRACK RBRACK
    | dims_opt LBRACK_RBRACK
    ;

/* =========================================================================
   7. STATEMENTS & BLOCKS
   ========================================================================= */

block
    : LBRACE blockStatements RBRACE
    ;

blockStatements
    : /* empty */
    | blockStatements blockStatement
    ;

blockStatement
    : localVariableDeclaration SEMI
    | statement
    | localTypeDeclaration
    ;

localVariableDeclaration
    : typeType variableDeclarators
    | VAR identifier ASSIGN expression
    | FINAL localVariableDeclaration
    | annotation localVariableDeclaration
    ;

localTypeDeclaration
    : classDeclaration
    | interfaceDeclaration
    | recordDeclaration
    | enumDeclaration
    ;

statement
    : block
    | IF LPAREN expression RPAREN statement %prec LOWER_THAN_ELSE
    | IF LPAREN expression RPAREN statement ELSE statement
    | FOR LPAREN forControl RPAREN statement
    | WHILE LPAREN expression RPAREN statement
    | DO statement WHILE LPAREN expression RPAREN SEMI
    | TRY block catchClauses
    | TRY block catchClauses_opt finallyBlock
    | TRY resourceSpecification block catchClauses_opt finallyBlock_opt
    | SWITCH LPAREN expression RPAREN switchBlock
    | SYNCHRONIZED LPAREN expression RPAREN block
    | RETURN expression_opt SEMI
    | THROW expression SEMI
    | BREAK identifier_opt SEMI
    | CONTINUE identifier_opt SEMI
    | YIELD expression SEMI
    | ASSERT expression SEMI
    | ASSERT expression COLON expression SEMI
    | expression SEMI
    | identifier COLON statement
    | SEMI
    ;

expression_opt
    : /* empty */
    | expression
    ;

identifier_opt
    : /* empty */
    | identifier
    ;

catchClauses_opt
    : /* empty */
    | catchClauses
    ;

catchClauses
    : catchClause
    | catchClauses catchClause
    ;

catchClause
    : CATCH LPAREN variableModifiers_opt catchType identifier RPAREN block
    ;

catchType
    : qualifiedName
    | catchType BITOR qualifiedName
    ;

finallyBlock_opt
    : /* empty */
    | finallyBlock
    ;

finallyBlock
    : FINALLY block
    ;

resourceSpecification
    : LPAREN resources semicolon_opt RPAREN
    ;

semicolon_opt
    : /* empty */
    | SEMI
    ;

resources
    : resource
    | resources SEMI resource
    ;

resource
    : localVariableDeclaration
    | postfixExpression
    ;

switchBlock
    : LBRACE RBRACE
    | LBRACE switchBlockStatementGroups RBRACE
    | LBRACE switchRules RBRACE
    ;

switchBlockStatementGroups
    : switchBlockStatementGroup
    | switchBlockStatementGroups switchBlockStatementGroup
    ;

switchBlockStatementGroup
    : switchLabels blockStatements
    ;

switchLabels
    : switchLabel
    | switchLabels switchLabel
    ;

switchLabel
    : CASE caseLabelElements guard_opt COLON
    | DEFAULT COLON
    | CASE DEFAULT COLON
    ;

caseLabelElements
    : caseLabelElement
    | caseLabelElements COMMA caseLabelElement
    ;

caseLabelElement
    : pattern
    | constantExpression
    | DEFAULT
    ;

constantExpression
    : constantPrimary
    | ADD constantExpression %prec UNARY
    | SUB constantExpression %prec UNARY
    | BANG constantExpression %prec UNARY
    | TILDE constantExpression %prec UNARY
    | constantExpression MUL constantExpression
    | constantExpression DIV constantExpression
    | constantExpression MOD constantExpression
    | constantExpression ADD constantExpression
    | constantExpression SUB constantExpression
    | constantExpression LSHIFT constantExpression
    | constantExpression RSHIFT constantExpression
    | constantExpression URSHIFT constantExpression
    | constantExpression BITAND constantExpression
    | constantExpression CARET constantExpression
    | constantExpression BITOR constantExpression
    ;

constantPrimary
    : literal
    | qualifiedName
    | LPAREN expression RPAREN
    ;

guard_opt
    : /* empty */
    | WHEN guardExpression
    ;

guardExpression
    : postfixExpression
    | INC guardExpression %prec PREFIX_OP
    | DEC guardExpression %prec PREFIX_OP
    | ADD guardExpression %prec UNARY
    | SUB guardExpression %prec UNARY
    | BANG guardExpression %prec UNARY
    | TILDE guardExpression %prec UNARY
    | LPAREN primitiveType dims_opt RPAREN guardExpression %prec UNARY
    | LPAREN classOrInterfaceType dims_opt RPAREN castOperand %prec UNARY
    | LPAREN typeType BITAND typeBoundList RPAREN guardExpression %prec UNARY
    | guardExpression MUL guardExpression
    | guardExpression DIV guardExpression
    | guardExpression MOD guardExpression
    | guardExpression ADD guardExpression
    | guardExpression SUB guardExpression
    | guardExpression LSHIFT guardExpression
    | guardExpression RSHIFT guardExpression
    | guardExpression URSHIFT guardExpression
    | guardExpression LT guardExpression
    | guardExpression GT guardExpression
    | guardExpression LE guardExpression
    | guardExpression GE guardExpression
    | guardExpression INSTANCEOF typeType
    | guardExpression INSTANCEOF pattern
    | guardExpression EQUAL guardExpression
    | guardExpression NOTEQUAL guardExpression
    | guardExpression BITAND guardExpression
    | guardExpression CARET guardExpression
    | guardExpression BITOR guardExpression
    | guardExpression AND guardExpression
    | guardExpression OR guardExpression
    | guardExpression QUESTION guardExpression COLON guardExpression
    ;

switchRules
    : switchRule
    | switchRules switchRule
    ;

switchRule
    : CASE caseLabelElements guard_opt ARROW switchRuleOutcome
    | DEFAULT ARROW switchRuleOutcome
    | CASE DEFAULT ARROW switchRuleOutcome
    ;

switchRuleOutcome
    : expression SEMI
    | block
    | THROW expression SEMI
    ;

forControl
    : enhancedForControl
    | forInit SEMI expression_opt SEMI forUpdate_opt
    | SEMI expression_opt SEMI forUpdate_opt
    ;

forInit
    : localVariableDeclaration
    | expressionList
    ;

forUpdate_opt
    : /* empty */
    | expressionList
    ;

enhancedForControl
    : typeType variableDeclaratorId COLON expression
    | variableModifiers typeType variableDeclaratorId COLON expression
    | VAR identifier COLON expression
    | variableModifiers VAR identifier COLON expression
    ;

/* =========================================================================
   8. EXPRESSIONS
   ========================================================================= */

expressionList_opt
    : /* empty */
    | expressionList
    ;

expressionList
    : expression
    | expressionList COMMA expression
    ;

expression
    : postfixExpression
    | INC expression %prec PREFIX_OP
    | DEC expression %prec PREFIX_OP
    | ADD expression %prec UNARY
    | SUB expression %prec UNARY
    | BANG expression %prec UNARY
    | TILDE expression %prec UNARY
    | LPAREN primitiveType dims_opt RPAREN expression %prec UNARY
    | LPAREN classOrInterfaceType dims_opt RPAREN castOperand %prec UNARY
    | LPAREN typeType BITAND typeBoundList RPAREN expression %prec UNARY
    | expression MUL expression
    | expression DIV expression
    | expression MOD expression
    | expression ADD expression
    | expression SUB expression
    | expression LSHIFT expression
    | expression RSHIFT expression
    | expression URSHIFT expression
    | expression LT expression
    | expression GT expression
    | expression LE expression
    | expression GE expression
    | expression INSTANCEOF typeType
    | expression INSTANCEOF pattern
    | expression EQUAL expression
    | expression NOTEQUAL expression
    | expression BITAND expression
    | expression CARET expression
    | expression BITOR expression
    | expression AND expression
    | expression OR expression
    | expression QUESTION expression COLON expression
    | expression ASSIGN expression
    | expression ADD_ASSIGN expression
    | expression SUB_ASSIGN expression
    | expression MUL_ASSIGN expression
    | expression DIV_ASSIGN expression
    | expression AND_ASSIGN expression
    | expression OR_ASSIGN expression
    | expression XOR_ASSIGN expression
    | expression MOD_ASSIGN expression
    | expression LSHIFT_ASSIGN expression
    | expression RSHIFT_ASSIGN expression
    | expression URSHIFT_ASSIGN expression
    | lambdaExpression
    ;

castOperand
    : primary
    | postfixExpression LBRACK expression RBRACK
    | postfixExpression LPAREN expressionList_opt RPAREN
    | postfixExpression DOT identifier
    | postfixExpression DOT THIS
    | postfixExpression DOT SUPER
    | postfixExpression DOT NEW typeArguments_opt identifier arguments classBody_opt
    | postfixExpression DOT explicitGenericInvocation
    | postfixExpression COLONCOLON typeArguments_opt identifier
    | postfixExpression COLONCOLON typeArguments_opt NEW
    | BANG expression %prec UNARY
    | TILDE expression %prec UNARY
    | lambdaExpression
    ;

postfixExpression
    : primary
    | postfixExpression LBRACK expression RBRACK
    | postfixExpression LPAREN expressionList_opt RPAREN
    | postfixExpression DOT identifier
    | postfixExpression DOT THIS
    | postfixExpression DOT SUPER
    | postfixExpression DOT NEW typeArguments_opt identifier arguments classBody_opt
    | postfixExpression DOT explicitGenericInvocation
    | postfixExpression COLONCOLON typeArguments_opt identifier
    | postfixExpression COLONCOLON typeArguments_opt NEW
    | postfixExpression INC %prec POSTFIX_OP
    | postfixExpression DEC %prec POSTFIX_OP
    ;

pattern
    : typeType identifier
    | variableModifiers typeType identifier
    | recordPattern
    ;

recordPattern
    : typeType LPAREN recordComponentPatternList_opt RPAREN
    ;

recordComponentPatternList_opt
    : /* empty */
    | recordComponentPatternList
    ;

recordComponentPatternList
    : pattern
    | recordComponentPatternList COMMA pattern
    ;

lambdaExpression
    : lambdaParameters ARROW lambdaBody %prec ARROW
    ;

lambdaParameters
    : identifier %prec ARROW
    | LPAREN formalParameterList_opt RPAREN
    | LPAREN identifierList RPAREN
    ;

identifierList
    : identifier COMMA identifier
    | identifierList COMMA identifier
    ;

lambdaBody
    : expression
    | block
    ;

explicitGenericInvocation
    : typeArguments identifier arguments
    ;



creator
    : nonWildcardTypeArguments_opt createdName arrayCreatorRest
    | nonWildcardTypeArguments_opt createdName classCreatorRest
    ;

nonWildcardTypeArguments_opt
    : /* empty */
    | typeArguments
    ;

createdName
    : identifier typeArgumentsOrDiamondList
    | primitiveType
    ;

typeArgumentsOrDiamondList
    : /* empty */
    | typeArguments
    | LT GT
    | typeArgumentsOrDiamondList DOT identifier typeArguments_opt
    | typeArgumentsOrDiamondList DOT identifier LT GT
    ;

classCreatorRest
    : arguments classBody_opt
    ;

arrayCreatorRest
    : dimExpressions
    | dimExpressions dims
    | dims arrayInitializer
    ;

dimExpressions
    : LBRACK expression RBRACK
    | dimExpressions LBRACK expression RBRACK
    ;

dims
    : LBRACK RBRACK
    | dims LBRACK RBRACK
    | LBRACK_RBRACK
    | dims LBRACK_RBRACK
    ;

arguments_opt
    : /* empty */
    | arguments
    ;

arguments
    : LPAREN expressionList_opt RPAREN
    ;

/* =========================================================================
   9. LITERALS & IDENTIFIERS
   ========================================================================= */

literal
    : DECIMAL_LITERAL
    | HEX_LITERAL
    | OCT_LITERAL
    | BINARY_LITERAL
    | FLOAT_LITERAL
    | HEX_FLOAT_LITERAL
    | BOOL_LITERAL
    | CHAR_LITERAL
    | STRING_LITERAL
    | TEXT_BLOCK
    | NULL_LITERAL
    ;

qualifiedName
    : identifier
    | qualifiedName DOT identifier
    ;

qualifiedNameList
    : qualifiedName
    | qualifiedNameList COMMA qualifiedName
    ;

identifier
    : IDENTIFIER
    | MODULE
    | OPEN
    | OPENS
    | REQUIRES
    | EXPORTS
    | TO
    | USES
    | PROVIDES
    | WHEN
    | WITH
    | TRANSITIVE
    | YIELD
    | SEALED
    | PERMITS
    | RECORD
    | VAR
    ;

%%

/* =========================================================================
   Bison Error Handler & Main Driver
   ========================================================================= */

void yyerror(const char *s) {
    syntax_error_occurred = 1;
    error_line = yylloc.first_line ? yylloc.first_line : yylineno;
}

#ifdef _WIN32
__declspec(dllexport)
#endif
int check_syntax(const char *filepath, char *err_msg, int err_msg_len) {
    syntax_error_occurred = 0;
    error_line = 0;
    yylineno = 1;
    current_column = 1;
    yylloc.first_line = 1;
    yylloc.first_column = 1;
    yylloc.last_line = 1;
    yylloc.last_column = 1;

    FILE *f = fopen(filepath, "r");
    if (!f) {
        if (err_msg && err_msg_len > 0) {
            snprintf(err_msg, err_msg_len, "ERROR: Could not open file '%s'", filepath);
        }
        return 2;
    }
    yyrestart(f);
    yyin = f;
    int result = yyparse();
    fclose(yyin);

    if (result == 0 && !syntax_error_occurred) {
        if (err_msg && err_msg_len > 0) {
            snprintf(err_msg, err_msg_len, "SUCCESS: Valid Java Syntax");
        }
        return 0;
    } else {
        if (err_msg && err_msg_len > 0) {
            snprintf(err_msg, err_msg_len, "ERROR: Line %d: Syntax error near '%s'",
                     error_line ? error_line : yylineno,
                     yytext ? yytext : "");
        }
        return 1;
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <file.java>\n", argv[0]);
        return 2;
    }
    char msg[512] = {0};
    int ret = check_syntax(argv[1], msg, sizeof(msg));
    if (ret == 0) {
        printf("%s\n", msg);
    } else {
        fprintf(stderr, "%s\n", msg);
    }
    return ret;
}
