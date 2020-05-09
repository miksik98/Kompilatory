class Node(object):
    pass


class Assign(Node):
    def __init__(self, var, op, expr, line):
        self.var = var
        self.op = op
        self.expr = expr
        self.line = line


class MatrixDeclaration(Node):
    def __init__(self, keyword, initValue, initValue2=None):
        self.initValue2 = initValue2
        self.keyword = keyword
        self.initValue = initValue


class Matrix(Node):
    def __init__(self, content, line):
        self.content = content
        self.line = line


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line


class Statement(Node):
    def __init__(self, body):
        self.body = body


class Statements(Node):
    def __init__(self, statementsList):
        self.statementsList = statementsList


class PrintExpressions(Node):
    def __init__(self, exprList):
        self.exprList = exprList

    def addExprList(self, exprList):
        self.exprList.extend(exprList)

    def addPrintExpr(self, expr):
        self.exprList.append(expr)


class PrintExpression(Node):
    def __init__(self, expr):
        self.expr = expr


class String(Node):
    def __init__(self, value):
        self.value = value


class MatrixRefAssign(Node):
    def __init__(self, var, ref, op, expr):
        self.var = var
        self.ref = ref
        self.op = op
        self.expr = expr


class UnaryOp(Node):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class BracketExpr(Node):
    def __init__(self, lParen, expr, rParen):
        self.lParen = lParen
        self.expr = expr
        self.rParen = rParen


class Condition(Node):
    def __init__(self, left, comp, right):
        self.left = left
        self.comp = comp
        self.right = right


class MainStatements(Node):
    def __init__(self, statementList):
        self.statementList = statementList

    def addStatementList(self, statementList):
        self.statementList.extend(statementList)

    def addStatement(self, statement):
        self.statementList.append(statement)


class WhileLoop(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body


class ForLoop(Node):
    def __init__(self, var, lRange, rRange, body):
        self.var = var
        self.lRange = lRange
        self.rRange = rRange
        self.body = body


class IfStatement(Node):
    def __init__(self, cond, ifBody, elseBody):
        self.cond = cond
        self.ifBody = ifBody
        self.elseBody = elseBody


class ElseStatement(Node):
    def __init__(self, body):
        self.body = body


class Empty(Node):
    pass


class Error(Node):
    def __init__(self, message):
        self.message = message

