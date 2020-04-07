import scanner
import ply.yacc as yacc
import numpy as np

# W tej wersji parsera zaimplementowano operacje na macierzach oraz na liczbach

tokens = scanner.tokens

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
    ('right', 'UMINUS'),
)

ids = {}


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_main_statements(p):
    """main_statements : LPARENCURLY statements RPARENCURLY main_statements
                      | main_statements LPARENCURLY statements RPARENCURLY
                      | main_statements main_statements
                      | statements"""


def p_loop_statement(p):
    """main_statements : loop_statement"""


def p_while_for(p):
    """loop_statement : WHILE LPAREN condition RPAREN loop_instruction_statement
                      | FOR ID ASSIGN num_expression RANGE num_expression loop_instruction_statement"""


def p_if(p):
    """main_statements : if_statement"""


def p_else_statement(p):
    """else_statement : ELSE instruction_statement
                      | ELSE if_statement"""


def p_if_statement(p):
    """if_statement : IF LPAREN condition RPAREN instruction_statement
                    | IF LPAREN condition RPAREN instruction_statement else_statement"""


def p_loop_statements(p):
    """loop_instruction_statement : LPARENCURLY main_statements_break_continue RPARENCURLY
                                  | statement SEMICOLON
                                  | BREAK SEMICOLON
                                  | CONTINUE SEMICOLON
                                  | loop_statement"""


def p_main_statements_break_continue(p):
    """main_statements_break_continue : main_statements
                                      | if_break_continue
                                      | main_statements_break_continue main_statements_break_continue
                                      | main_statements_break_continue CONTINUE SEMICOLON main_statements_break_continue
                                      | main_statements_break_continue BREAK SEMICOLON main_statements_break_continue
                                      | empty"""


def p_else_break_continue(p):
    """else_break_continue : ELSE instruction_statement_break_continue
                           | ELSE if_break_continue"""


def p_if_break_continue(p):
    """if_break_continue : IF LPAREN condition RPAREN instruction_statement_break_continue
                         | IF LPAREN condition RPAREN instruction_statement_break_continue else_break_continue"""


def p_instruction_statement_break_continue(p):
    """instruction_statement_break_continue : LPARENCURLY main_statements_break_continue RPARENCURLY
                                            | LPARENCURLY empty RPARENCURLY
                                            | statement SEMICOLON
                                            | BREAK SEMICOLON
                                            | CONTINUE SEMICOLON"""


def p_instruction_statement(p):
    """instruction_statement : LPARENCURLY main_statements RPARENCURLY
                             | LPARENCURLY empty RPARENCURLY
                             | statement SEMICOLON"""


def p_condition(p):
    """condition : num_expression EQUALITY num_expression
                 | num_expression INEQUALITY num_expression
                 | num_expression GREATER num_expression
                 | num_expression GREATER_EQUAL num_expression
                 | num_expression LESS num_expression
                 | num_expression LESS_EQUAL num_expression"""
    if p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '>=':
        p[0] = p[1] != p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]


def p_statements(p):
    """statements : statement SEMICOLON statements
                  | statement SEMICOLON"""


def p_print(p):
    """statement : PRINT print_expression"""
    print(p[2])


def p_print_expression(p):
    """print_expression : expression
                        | print_expression COMMA print_expression"""


def p_expression(p):
    """expression : num_expression
                  | matrix_expression"""
    p[0] = p[1]


def p_string(p):
    """expression : STRING"""
    p[0] = p[1][1:len(p[1]) - 1]


def p_assign_num(p):
    """statement : ID ASSIGN num_expression"""
    ids[p[1]] = p[3]


def p_assign_cell_matrix(p):
    """statement : ID MATRIX ASSIGN num_expression"""
    ids[p[1]][p[2].item(0)][p[2].item(1)] = p[4]


def p_add_assign_cell_matrix(p):
    """statement : ID MATRIX ADDASSIGN num_expression"""
    ids[p[1]][p[2].item(0)][p[2].item(1)] += p[4]


def p_sub_assign_cell_matrix(p):
    """statement : ID MATRIX SUBASSIGN num_expression"""
    ids[p[1]][p[2].item(0)][p[2].item(1)] -= p[4]


def p_mul_assign_cell_matrix(p):
    """statement : ID MATRIX MULASSIGN num_expression"""
    ids[p[1]][p[2].item(0)][p[2].item(1)] *= p[4]


def p_div_assign_cell_matrix(p):
    """statement : ID MATRIX DIVASSIGN num_expression"""
    ids[p[1]][p[2].item(0)][p[2].item(1)] /= p[4]


def p_assign_matrix(p):
    """statement : ID ASSIGN matrix_expression"""
    ids[p[1]] = p[3]


def p_assign_num_compound(p):
    """statement : ID ADDASSIGN num_expression
                  | ID SUBASSIGN num_expression
                  | ID MULASSIGN num_expression
                  | ID DIVASSIGN num_expression"""
    if p[2] == '+=':
        ids[p[1]] += p[3]
    elif p[2] == '-=':
        ids[p[1]] -= p[3]
    elif p[2] == '*=':
        ids[p[1]] *= p[3]
    elif p[2] == '/=':
        ids[p[1]] /= p[3]


def p_num_expression_name(p):
    """num_expression : ID"""
    try:
        pass
        p[0] = ids[p[1]]
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        p[0] = 0


def p_matrix_expression_name(p):
    """matrix_expression : ID"""
    try:
        pass
        p[0] = ids[p[1]]
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        p[0] = 0


def p_num_expression_group(p):
    """num_expression : LPAREN num_expression RPAREN"""
    p[0] = p[2]


def p_matrix_expression_group(p):
    """matrix_expression : LPAREN matrix_expression RPAREN"""
    p[0] = p[2]


def p_num_expression_binop(p):
    """num_expression : num_expression ADD num_expression
                  | num_expression SUB num_expression
                  | num_expression MUL num_expression
                  | num_expression DIV num_expression"""
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_matrix_expression_binop(p):
    """matrix_expression : matrix_expression ADD matrix_expression
                  | matrix_expression SUB matrix_expression
                  | matrix_expression MUL matrix_expression
                  | matrix_expression DIV matrix_expression"""
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_matrix_expression_binop_element_wise(p):
    """matrix_expression : matrix_expression DOTADD matrix_expression
                  | matrix_expression DOTSUB matrix_expression
                  | matrix_expression DOTMUL matrix_expression
                  | matrix_expression DOTDIV matrix_expression"""
    if p[2] == '.+':
        p[0] = np.add(p[1], p[3])
    elif p[2] == '.-':
        p[0] = np.subtract(p[1], p[3])
    elif p[2] == '.*':
        p[0] = np.multiply(p[1], p[3])
    elif p[2] == './':
        p[0] = np.divide(p[1], p[3])


def p_matrix_assign_compound(p):
    """statement : ID ADDASSIGN matrix_expression
                  | ID SUBASSIGN matrix_expression
                  | ID MULASSIGN matrix_expression
                  | ID DIVASSIGN matrix_expression"""
    if p[2] == '+=':
        ids[p[1]] += p[3]
    elif p[2] == '-=':
        ids[p[1]] -= p[3]
    elif p[2] == '*=':
        ids[p[1]] *= p[3]
    elif p[2] == '/=':
        ids[p[1]] /= p[3]


def p_num_expression_uminus(p):
    """num_expression : SUB num_expression %prec UMINUS"""
    p[0] = -p[2]


def p_matrix_expression_uminus(p):
    """matrix_expression : SUB matrix_expression %prec UMINUS"""
    p[0] = -p[2]


def p_matrix_transpose(p):
    """matrix_expression : matrix_expression TRANSPOSE"""
    p[0] = p[1].transpose()


def p_num_expression(p):
    """num_expression : INTNUM
                      | FLOATNUM"""
    p[0] = p[1]


def p_matrix_zeros_expression(p):
    """matrix_expression : ZEROS LPAREN INTNUM RPAREN"""
    p[0] = np.zeros((p[3], p[3]))


def p_matrix_ones_expression(p):
    """matrix_expression : ONES LPAREN INTNUM RPAREN"""
    p[0] = np.ones((p[3], p[3]), dtype=np.int32)


def p_matrix_eye_expression(p):
    """matrix_expression : EYE LPAREN INTNUM RPAREN"""
    p[0] = np.eye(p[3], dtype=np.int32)


def p_matrix_explicit(p):
    """matrix_expression : MATRIX"""
    p[0] = p[1]


def p_return(p):
    """statement : return_statement"""


def p_return_statement(p):
    """return_statement : RETURN expression"""


def p_empty(p):
    """empty :"""


parser = yacc.yacc()
