import AST

variables = {}


class MatrixShape:
    def __init__(self, length, width):
        self.length = length
        self.width = width


class Number:
    pass


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):

    def visit_BinExpr(self, node):
        op = node.op
        method_left = 'visit_' + node.left.__class__.__name__
        left_visitor = getattr(self, method_left, self.generic_visit)
        value1 = (left_visitor(node.left))
        method_right = 'visit_' + node.right.__class__.__name__
        right_visitor = getattr(self, method_right, self.generic_visit)
        value2 = (right_visitor(node.right))
        type1 = type(value1)
        type2 = type(value2)
        if type1 == MatrixShape and type2 == MatrixShape:
            if op in ['+', '-', '/'] or op[0] == '.':
                if value1.length != value2.length or value1.width != value2.width:
                    print("Incompatible shapes of matrices at line", node.line)
            elif op == '*':
                if value1.width != value2.length:
                    print("Incompatible shapes of matrices at line", node.line)
                else:
                    return MatrixShape(value1.length, value2.width)
        if type1 != type2:
            print("Incompatible types at line", node.line)
        return value1

    def visit_Variable(self, node):
        return variables[node.name]

    def visit_NoneType(self, node):
        pass

    def visit_Assign(self, node):
        op = node.op
        method = 'visit_' + node.expr.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        expr = visitor(node.expr)
        if op == '=':
            variables[node.var.name] = expr
        else:
            if node.var.name not in variables:
                print("Undeclared variable at line", node.line)
            else:
                var = variables[node.var.name]
                type1 = type(var)
                type2 = type(expr)
                if type1 == MatrixShape and type2 == MatrixShape:
                    if op[0] in ['+', '-', '/']:
                        if var.length != expr.length or var.width != expr.width:
                            print("Incompatible shapes of matrices at line", node.line)
                    elif op[0] == '*':
                        if var.width != expr.length:
                            print("Incompatible shapes of matrices at line", node.line)
                        else:
                            expr = MatrixShape(var.length, expr.width)
                if type1 != type2:
                    print("Incompatible types at line", node.line)
                variables[node.var.name] = expr

    def visit_MatrixDeclaration(self, node):
        if node.keyword == 'eye':
            return MatrixShape(node.initValue, node.initValue)
        elif node.keyword == 'ones':
            return MatrixShape(node.initValue, node.initValue2)
        else:
            return MatrixShape(node.initValue, node.initValue2)

    def visit_IntNum(self, node):
        return Number()

    def visit_FloatNum(self, node):
        return Number()

    def visit_Matrix(self, node):
        if node.content.dtype == object:
            print("Wrong Matrix Declaration at line", node.line)
        return MatrixShape(node.content.shape[0], node.content.shape[1])

    def visit_Statement(self, node):
        if isinstance(node, AST.Statements):
            self.visit_Statements(node)
        else:
            method = 'visit_' + node.body.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            visitor(node.body)

    def visit_Statements(self, node):
        for i in node.statementsList:
            self.visit_Statement(i)

    def visit_PrintExpressions(self, node):
        pass

    def visit_PrintExpression(self, node):
        pass

    def visit_String(self, node):
        return node

    def visit_MatrixRefAssign(self, node):
        pass

    def visit_UnaryOp(self, node):
        method = 'visit_' + node.expr.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        expr = visitor(node.expr)
        if type(expr) == MatrixShape and node.op == '\'':
            return MatrixShape(expr.width, expr.length)

    def visit_BracketExpr(self, node):
        pass

    def visit_Condition(self, node):
        pass

    def visit_MainStatements(self, node):
        for i in node.statementList:
            self.visit_Statement(i)

    def visit_WhileLoop(self, node):
        pass

    def visit_ForLoop(self, node):
        pass

    def visit_IfStatement(self, node):
        pass

    def visit_ElseStatement(self, node):
        pass

    def visit_Empty(self, node):
        pass

    def visit_Error(self, node):
        pass
