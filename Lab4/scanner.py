import ply.lex as lex
from numpy import matrix

# First character of current line number
column_offset = 0

# Dict of keywords
keywords = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'print': 'PRINT',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
}

# Tokens definition
tokens = [
             'INTNUM',
             'ADD',
             'DOTADD',
             'ADDASSIGN',
             'SUB',
             'DOTSUB',
             'SUBASSIGN',
             'MUL',
             'DOTMUL',
             'MULASSIGN',
             'DIV',
             'DOTDIV',
             'DIVASSIGN',
             'ASSIGN',
             'LPAREN',
             'RPAREN',
             'LPARENSQUARE',
             'RPARENSQUARE',
             'LPARENCURLY',
             'RPARENCURLY',
             'COMMENT',
             'EQUALITY',
             'INEQUALITY',
             'GREATER',
             'GREATER_EQUAL',
             'LESS',
             'LESS_EQUAL',
             'RANGE',
             'TRANSPOSE',
             'COMMA',
             'SEMICOLON',
             'FLOATNUM',
             'STRING',
             'ID',
             'MATRIX',
             'REF'
         ] + list(keywords.values())

# Regular expression rules for simple tokens
t_ADD = r'\+'
t_DOTADD = r'\.\+'
t_ADDASSIGN = r'\+='
t_SUB = r'-'
t_DOTSUB = r'\.-'
t_SUBASSIGN = r'-='
t_MUL = r'\*'
t_DOTMUL = r'\.\*'
t_MULASSIGN = r'\*='
t_DIV = r'/'
t_DOTDIV = r'\./'
t_DIVASSIGN = r'/='
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LPARENSQUARE = r'\['
t_RPARENSQUARE = r'\]'
t_LPARENCURLY = r'\{'
t_RPARENCURLY = r'\}'
t_COMMENT = r'\#.*\n*'
t_EQUALITY = r'=='
t_INEQUALITY = r'!='
t_GREATER = r'>'
t_GREATER_EQUAL = r'>='
t_LESS = r'<'
t_LESS_EQUAL = r'<='
t_RANGE = r':'
t_TRANSPOSE = r'\''
t_COMMA = r','
t_SEMICOLON = r';'
t_STRING = r'".*"'


# Regular expression rules with some action code
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'  # _var, var, var_description1 etc
    if t.value in keywords.keys():
        t.type = keywords[t.value]
    else:
        t.type = "ID"
    return t


def t_FLOATNUM(t):
    r'(((\d*\.\d+)|(\d+\.\d*))(E(-)?\d+)?)|(\d+E(-)?\d+)'  # 0.5, .5, 20., 20E2, 0.5E2, .5E2, 20.E2 etc
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_MATRIX(t):
    r'((\[(\s)*(\[(\s)*(\d+(\s)*\,(\s)*)*\d+(\s)*\](\s)*\,(\s)*)*(\[((\s)*\d+(\s)*\,(\s)*)*\d+(\s)*\])(\s)*\]))'
    count = 0
    for i in t.value:
        if i == '[':
            count = count + 1
        if i == '\n':
            t.lexer.lineno += 1
    if count > 1:
        import ast
        t.value = matrix(ast.literal_eval(t.value))
    else:
        t.value = matrix(t.value)
    return t


def t_REF(t):
    r'\[(\s)*\d+(\s)*\,(\s)*\d+(\s)*\]'
    import ast
    t.value = ast.literal_eval(t.value)
    return t


# Rule for tracking line numbers by newline character or comment
def t_newline(t):
    r'(\#.*\n*)|\n+'
    global column_offset
    i = 0
    for c in t.value:
        if c == '\n':
            i = i + 1
    t.lexer.lineno += i
    column_offset = t.lexer.lexpos


# Ignore whitespaces
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("\033[1;31;40mIllegal character '%s' at (%d,%d)" % (t.value[0], t.lineno, t.lexpos - column_offset + 1))
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


# Current column
def find_column(tok):
    return tok.lexpos - column_offset + 1
