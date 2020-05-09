from __future__ import print_function
import AST
from numpy import matrix

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print('| '*indent + str(self.value))

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
        # fill in the body

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print('| '*indent + str(self.value))

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print('| '*indent + self.op)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        print('| '*indent + self.op)
        self.var.printTree(indent+1)
        self.expr.printTree(indent+1)

    @addToClass(AST.MatrixDeclaration)
    def printTree(self, indent=0):
        print('| ' * indent + self.keyword)
        self.initValue.printTree(indent+1)

    @addToClass(AST.Statements)
    def printTree(self, indent=0):
        for statement in self.statementsList:
            statement.printTree(indent)

    @addToClass(AST.Statement)
    def printTree(self, indent=0):
        self.body.printTree(indent)

    @addToClass(AST.PrintExpressions)
    def printTree(self, indent=0):
        print('| '*indent+'PRINT')
        for printExpr in self.exprList:
            printExpr.printTree(indent+1)

    @addToClass(AST.PrintExpression)
    def printTree(self, indent=0):
        self.expr.printTree(indent)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print('| '*indent+self.name)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print('| ' * indent + self.value)

    @addToClass(AST.MatrixRefAssign)
    def printTree(self, indent=0):
        print('| ' * indent + self.op)
        print('| ' * (indent+1) + 'REF')
        self.var.printTree(indent+2)
        print('| ' * (indent + 2) + str(self.ref[0]))
        print('| ' * (indent + 2) + str(self.ref[1]))
        self.expr.printTree(indent + 1)

    @addToClass(matrix)
    def printTree(self, indent=0):
        print('| ' * indent + 'VECTOR')
        indent = indent + 1
        for i in range(0, self.shape[0]):
            print('| ' * indent + 'VECTOR')
            for elem in self[i].flat:
                print('| ' * (indent+1) + str(elem))

    @addToClass(AST.UnaryOp)
    def printTree(self, indent=0):
        if self.op == '\'':
            print('| ' * indent + 'TRANSPOSE')
        else:
            print('| ' * indent + self.op)
        self.expr.printTree(indent + 1)

    @addToClass(AST.BracketExpr)
    def printTree(self, indent=0):
        print('| ' * indent + self.lParen)
        self.expr.printTree(indent+1)
        print('| ' * indent + self.rParen)

    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        print('| ' * indent + self.comp)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.MainStatements)
    def printTree(self, indent=0):
        for s in self.statementList:
            s.printTree(indent)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        print('| ' * indent + 'WHILE')
        self.cond.printTree(indent+1)
        self.body.printTree(indent+1)

    @addToClass(AST.Empty)
    def printTree(self, indent=0):
        pass

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        print('| ' * indent + 'FOR')
        self.var.printTree(indent+1)
        print('| ' * (indent+1) + 'RANGE')
        self.lRange.printTree(indent+2)
        self.rRange.printTree(indent+2)
        self.body.printTree(indent+1)

    @addToClass(AST.IfStatement)
    def printTree(self, indent=0):
        print('| ' * indent + 'IF')
        self.cond.printTree(indent+1)
        print('| ' * indent + 'THEN')
        self.ifBody.printTree(indent+1)
        if type(self.elseBody) != AST.Empty:
            self.elseBody.printTree(indent)

    @addToClass(AST.ElseStatement)
    def printTree(self, indent=0):
        print('| ' * indent + 'ELSE')
        self.body.printTree(indent+1)
