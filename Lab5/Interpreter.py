import AST
import Exceptions
from Memory import *
from visit import *
import sys
import numpy as np
import copy

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.globalMemory = Memory("globalMemory")
        # stack localMemory - i+1 element contains i element's variables
        self.localMemory = [MemoryStack(self.globalMemory)]

    # get from top of stack
    def memory(self):
        return self.localMemory[len(self.localMemory) - 1]

    @on('node')
    def visit(self, node):
        pass

    @when(AST.MainStatements)
    def visit(self, node):
        for statement in node.statementList:
            statement.accept(self)

    @when(AST.Statement)
    def visit(self, node):
        node.body.accept(self)

    @when(AST.Assign)
    def visit(self, node):
        name = node.var.name
        op = node.op
        value = node.expr.accept(self)

        if op == '=':
            self.memory().insert(name, value)
            return
        # because of matrices operations .+, .- etc
        op0 = op[0]

        if op0 == '+':
            self.memory().set(name, self.memory().get(name) + value)
        if op0 == '-':
            self.memory().set(name, self.memory().get(name) - value)
        if op0 == '*':
            self.memory().set(name, self.memory().get(name) * value)
        if op0 == '/':
            self.memory().set(name, self.memory().get(name) / value)

    @when(AST.Variable)
    def visit(self, node):
        return self.memory().get(node.name)

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # because of matrices operations .+, .- etc
        op = node.op[len(node.op) - 1]

        if op == '+':
            return r1 + r2
        if op == '-':
            return r1 - r2
        if op == '*':
            return r1 * r2
        if op == '/':
            return r1 / r2

    @when(AST.Statements)
    def visit(self, node):
        for statement in node.statementsList:
            statement.accept(self)

    @when(AST.MatrixDeclaration)
    def visit(self, node):
        if node.keyword == 'ones':
            if node.initValue2 is not None:
                return np.ones(node.initValue.accept(self), node.initValue2.accept(self))
            else:
                return np.ones(node.initValue.accept(self))
        if node.keyword == 'zeros':
            if node.initValue2 is not None:
                return np.zeros(node.initValue.accept(self), node.initValue2.accept(self))
            else:
                return np.zeros(node.initValue.accept(self))
        if node.keyword == 'eye':
            if node.initValue2 is not None:
                return np.eye(node.initValue.accept(self), node.initValue2.accept(self))
            else:
                return np.eye(node.initValue.accept(self))

    @when(AST.Matrix)
    def visit(self, node):
        return node.content

    @when(AST.ElseStatement)
    def visit(self, node):
        elseMemory = copy.deepcopy(self.memory())
        self.localMemory.append(elseMemory)
        try:
            node.ifBody.accept(self)
            self.localMemory.remove(elseMemory)
        except Exceptions.BreakException:
            self.localMemory.remove(elseMemory)
            raise Exceptions.BreakException  # exception should be caught in loop
        except Exceptions.ContinueException:
            self.localMemory.remove(elseMemory)
            raise Exceptions.ContinueException  # same

    @when(AST.UnaryOp)
    def visit(self, node):
        op = node.op
        expr = node.expr.accept(self)
        if op == '\'':
            return np.transpose(expr)
        if op == '-':
            return -expr
        if op == 'break':
            raise Exceptions.BreakException()
        if op == 'continue':
            raise Exceptions.ContinueException()
        if op == 'return':
            raise Exceptions.ReturnValueException(node.expr.accept(self))

    @when(AST.IfStatement)
    def visit(self, node):
        if node.cond.accept(self):
            ifMemory = copy.deepcopy(self.memory())
            self.localMemory.append(ifMemory)
            try:
                node.ifBody.accept(self)
                self.localMemory.remove(ifMemory)
            except Exceptions.BreakException:
                self.localMemory.remove(ifMemory)
                raise Exceptions.BreakException
            except Exceptions.ContinueException:
                self.localMemory.remove(ifMemory)
                raise Exceptions.ContinueException
        else:
            node.elseBody.accept(self)

    @when(AST.Empty)
    def visit(self, node):
        return None

    @when(AST.Condition)
    def visit(self, node):
        left = node.left.accept(self)
        comp = node.comp
        right = node.right.accept(self)
        if comp == '==':
            return left == right
        if comp == '>':
            return left > right
        if comp == '>=':
            return left >= right
        if comp == '<':
            return left < right
        if comp == '<=':
            return left <= right

    @when(AST.ForLoop)
    def visit(self, node):
        name = node.var.name
        lRange = node.lRange.accept(self)
        rRange = node.rRange.accept(self)
        forMemory = copy.deepcopy(self.memory())
        self.localMemory.append(forMemory)
        self.memory().insert(name, lRange)
        r = None
        ended = False  # variable used to correctly handle continue exception
        while not ended:
            try:
                while self.memory().get(name) < rRange:
                    r = node.body.accept(self)
                    self.memory().set(name, self.memory().get(name) + 1)
                self.localMemory.remove(forMemory)
                ended = True
            except Exceptions.BreakException:
                ended = True
                self.localMemory.remove(forMemory)
            except Exceptions.ContinueException:
                pass
        return r

    @when(AST.BracketExpr)
    def visit(self, node):
        return node.expr.accept(self)

    @when(AST.MatrixRefAssign)
    def visit(self, node):
        matrix = node.var.accept(self)
        ref = node.ref
        matrix[ref[0], ref[1]] = node.expr.accept(self)
        self.memory().insert(node.var.name, matrix)

    @when(AST.String)
    def visit(self, node):
        return node.value[1:-1]

    @when(AST.PrintExpression)
    def visit(self, node):
        print(node.expr.accept(self))

    @when(AST.PrintExpressions)
    def visit(self, node):
        for expr in node.exprList:
            expr.accept(self)

    @when(AST.WhileLoop)
    def visit(self, node):
        ended = False  # variable used to correctly handle continue exception
        whileMemory = copy.deepcopy(self.memory())
        self.localMemory.append(whileMemory)
        while not ended:
            try:
                while node.cond.accept(self):
                    node.body.accept(self)
                self.localMemory.remove(whileMemory)
                ended = True
            except Exceptions.BreakException:
                self.localMemory.remove(whileMemory)
                ended = True
            except Exceptions.ContinueException:
                pass
