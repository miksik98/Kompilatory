import scanner
import ply.yacc as yacc
import AST

tokens = scanner.tokens

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
    ('right', 'UMINUS'),
    ('right', 'TRANSPOSE'),
)


def p_error(p):
    if p:
        if p.type != 'SEMICOLON':
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_column(p),
                                                                                             p.type, p.value))
        parser.errok()
    else:
        print("Unexpected end of input")


def p_main_statements(p):
    """main_statements : LPARENCURLY statements RPARENCURLY main_statements
                      | main_statements LPARENCURLY statements RPARENCURLY
                      | main_statements main_statements
                      | statements"""
    if len(p) == 2:
        p[0] = AST.MainStatements([p[1]])
    elif len(p) == 3:
        t = AST.MainStatements([])
        t.addStatementList(p[1].statementList)
        t.addStatementList(p[2].statementList)
        p[0] = t
    else:
        if p[1] == '{':
            t = AST.MainStatements([])
            t.addStatementList([p[2]])
            t.addStatementList(p[4].statementList)
            p[0] = t
        else:
            t = AST.MainStatements([])
            t.addStatementList([p[3]])
            t.addStatementList(p[1].statementList)
            p[0] = t


def p_loop_statement(p):
    """main_statements : loop_statement
                       | if_statement"""
    p[0] = AST.MainStatements([p[1]])


def p_while(p):
    """loop_statement : WHILE LPAREN condition RPAREN loop_instruction_statement"""
    p[0] = AST.WhileLoop(p[3], p[5])


def p_for(p):
    """loop_statement : FOR ID ASSIGN num_expression RANGE num_expression loop_instruction_statement"""
    p[0] = AST.ForLoop(AST.Variable(p[2]), p[4], p[6], p[7])


def p_if_statement(p):
    """if_statement : IF LPAREN condition RPAREN instruction_statement
                    | IF LPAREN condition RPAREN instruction_statement else_statement"""
    if len(p) == 7:
        p[0] = AST.IfStatement(p[3], AST.MainStatements(p[5].statementList), p[6])
    else:
        p[0] = AST.IfStatement(p[3], AST.MainStatements(p[5].statementList), AST.Empty())


def p_else_statement(p):
    """else_statement : ELSE instruction_statement
                      | ELSE if_statement"""
    p[0] = AST.ElseStatement(p[2])


def p_loop_statements(p):
    """loop_instruction_statement : LPARENCURLY main_statements_break_continue RPARENCURLY
                                  | statement SEMICOLON
                                  | loop_statement"""
    if len(p) == 4:
        t = AST.MainStatements([])
        t.addStatementList(p[2].statementList)
        p[0] = t
    else:
        p[0] = AST.MainStatements([p[1]])


def p_loop_only_break_continue(p):
    """loop_instruction_statement : BREAK SEMICOLON
                                  | CONTINUE SEMICOLON"""
    p[0] = AST.MainStatements([AST.UnaryOp(p[1], AST.Empty())])


def p_main_statements_break_continue(p):
    """main_statements_break_continue : main_statements
                                      | if_break_continue
                                      | main_statements_break_continue main_statements_break_continue
                                      | main_statements_break_continue CONTINUE SEMICOLON main_statements_break_continue
                                      | main_statements_break_continue BREAK SEMICOLON main_statements_break_continue
                                      | empty"""
    if len(p) == 2:
        p[0] = AST.MainStatements([p[1]])
    elif len(p) == 3:
        p[0] = AST.MainStatements([p[1], p[2]])
    else:
        p[0] = AST.MainStatements([p[1], AST.UnaryOp(p[2], AST.Empty()), p[4]])


def p_else_break_continue(p):
    """else_break_continue : ELSE instruction_statement_break_continue
                           | ELSE if_break_continue"""
    p[0] = AST.ElseStatement(p[2])


def p_if_break_continue(p):
    """if_break_continue : IF LPAREN condition RPAREN instruction_statement_break_continue
                         | IF LPAREN condition RPAREN instruction_statement_break_continue else_break_continue"""
    if len(p) == 7:
        p[0] = AST.IfStatement(p[3], AST.MainStatements(p[5].statementList), p[6])
    else:
        p[0] = AST.IfStatement(p[3], AST.MainStatements(p[5].statementList), AST.Empty())


def p_instruction_statement_break_continue1(p):
    """instruction_statement_break_continue : LPARENCURLY main_statements_break_continue RPARENCURLY
                                            | LPARENCURLY empty RPARENCURLY
                                            | statement SEMICOLON"""
    if len(p) == 4:
        p[0] = AST.MainStatements([p[2]])
    else:
        p[0] = AST.MainStatements([p[1]])


def p_instruction_statement_break_continue2(p):
    """instruction_statement_break_continue : BREAK SEMICOLON
                                            | CONTINUE SEMICOLON"""
    p[0] = AST.MainStatements([AST.UnaryOp(p[1], AST.Empty())])


def p_instruction_statement(p):
    """instruction_statement : LPARENCURLY main_statements RPARENCURLY
                             | LPARENCURLY empty RPARENCURLY
                             | statement SEMICOLON"""
    if len(p) == 3:
        p[0] = AST.MainStatements([p[1]])
    elif type(p[2]) == AST.Empty:
        p[0] = AST.MainStatements([p[2]])
    else:
        p[0] = p[2]

def p_condition(p):
    """condition : num_expression EQUALITY num_expression
                 | num_expression INEQUALITY num_expression
                 | num_expression GREATER num_expression
                 | num_expression GREATER_EQUAL num_expression
                 | num_expression LESS num_expression
                 | num_expression LESS_EQUAL num_expression"""
    p[0] = AST.Condition(p[1], p[2], p[3])


def p_condintion_group(p):
    """condition : LPAREN condition RPAREN"""
    p[0] = p[2]


def p_statements(p):
    """statements : statement SEMICOLON statements
                  | statement SEMICOLON"""
    if len(p) == 3:
        p[0] = AST.Statement(p[1])
    else:
        p[0] = AST.Statements([AST.Statement(p[1]), AST.Statement(p[3])])


def p_print(p):
    """statement : PRINT print_expression"""
    t = AST.PrintExpressions([])
    t.addExprList(p[2].exprList)
    p[0] = t


def p_print_expression(p):
    """print_expression : expression
                        | expression COMMA print_expression"""
    if len(p) == 2:
        p[0] = AST.PrintExpressions([AST.PrintExpression(p[1])])
    else:
        t = AST.PrintExpressions([AST.PrintExpression(p[1])])
        t.addExprList(p[3].exprList)
        p[0] = t


def p_expression(p):
    """expression : num_expression
                  | matrix_expression"""
    p[0] = p[1]


def p_expression_string(p):
    """expression : STRING"""
    p[0] = AST.String(p[1])


def p_assign_string(p):
    """statement : ID ASSIGN STRING"""
    p[0] = AST.Assign(AST.Variable(p[1]), p[2], AST.String(p[3]), p.lineno(2))


def p_assign_cell_matrix(p):
    """statement : ID REF ASSIGN num_expression
                 | ID REF ADDASSIGN num_expression
                 | ID REF SUBASSIGN num_expression
                 | ID REF MULASSIGN num_expression
                 | ID REF DIVASSIGN num_expression"""
    p[0] = AST.MatrixRefAssign(AST.Variable(p[1]), p[2], p[3], p[4])


def p_assign_num(p):
    """statement : ID ASSIGN num_expression
                 | ID ADDASSIGN num_expression
                 | ID SUBASSIGN num_expression
                 | ID MULASSIGN num_expression
                 | ID DIVASSIGN num_expression"""
    p[0] = AST.Assign(AST.Variable(p[1]), p[2], p[3], p.lineno(2))


def p_num_expression_name(p):
    """num_expression : ID"""
    p[0] = AST.Variable(p[1])


def p_matrix_expression_name(p):
    """matrix_expression : ID"""
    p[0] = AST.Variable(p[1])


def p_num_expression_group(p):
    """num_expression : LPAREN num_expression RPAREN"""
    p[0] = AST.BracketExpr(p[1], p[2], p[3])


def p_matrix_expression_group(p):
    """matrix_expression : LPAREN matrix_expression RPAREN"""
    p[0] = AST.BracketExpr(p[1], p[2], p[3])


def p_num_expression_binop(p):
    """num_expression : num_expression ADD num_expression
                  | num_expression SUB num_expression
                  | num_expression MUL num_expression
                  | num_expression DIV num_expression"""
    p[0] = AST.BinExpr(p[2], p[1], p[3], p.lineno(2))


def p_matrix_expression_binop(p):
    """matrix_expression : matrix_expression ADD matrix_expression
                         | matrix_expression SUB matrix_expression
                         | matrix_expression MUL matrix_expression
                         | matrix_expression DIV matrix_expression
                         | matrix_expression DOTADD matrix_expression
                         | matrix_expression DOTSUB matrix_expression
                         | matrix_expression DOTMUL matrix_expression
                         | matrix_expression DOTDIV matrix_expression"""
    p[0] = AST.BinExpr(p[2], p[1], p[3], p.lineno(2))


def p_matrix_assign(p):
    """statement : ID ASSIGN matrix_expression
                 | ID ADDASSIGN matrix_expression
                 | ID SUBASSIGN matrix_expression
                 | ID MULASSIGN matrix_expression
                 | ID DIVASSIGN matrix_expression"""
    p[0] = AST.Assign(AST.Variable(p[1]), p[2], p[3], p.lineno(2))


def p_num_expression_uminus(p):
    """num_expression : SUB num_expression %prec UMINUS"""
    p[0] = AST.UnaryOp(p[1], p[2])


def p_matrix_expression_uminus(p):
    """matrix_expression : SUB matrix_expression %prec UMINUS"""
    p[0] = AST.UnaryOp(p[1], p[2])


def p_matrix_transpose(p):
    """matrix_expression : matrix_expression TRANSPOSE"""
    p[0] = AST.UnaryOp(p[2], p[1])


def p_num_expression_int(p):
    """num_expression : INTNUM"""
    p[0] = AST.IntNum(p[1])


def p_num_expression_float(p):
    """num_expression : FLOATNUM"""
    p[0] = AST.FloatNum(p[1])


def p_matrix_keyword_declaration_expression(p):
    """matrix_expression : ZEROS LPAREN num_expression RPAREN
                         | ONES LPAREN  num_expression RPAREN
                         | EYE LPAREN num_expression RPAREN"""
    p[0] = AST.MatrixDeclaration(p[1], p[3])


def p_matrix_keyword_declaration_expression_2args(p):
    """matrix_expression : ONES LPAREN  num_expression COMMA num_expression RPAREN
                         | ZEROS LPAREN num_expression COMMA num_expression RPAREN"""
    p[0] = AST.MatrixDeclaration(p[1], p[3], p[5])


def p_matrix_explicit(p):
    """matrix_expression : MATRIX"""
    p[0] = AST.Matrix(p[1], p.lineno(1))


def p_return(p):
    """statement : return_statement"""
    p[0] = p[1]


def p_return_statement(p):
    """return_statement : RETURN expression"""
    p[0] = AST.UnaryOp(p[1], p[2])


def p_empty(p):
    """empty :"""
    p[0] = AST.Empty()


parser = yacc.yacc()
