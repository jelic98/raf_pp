class AST(object):
    pass

class Program(AST):
    def __init__(self, child_nodes):
        self.child_nodes = child_nodes

class Fun_Decl(AST):
    def __init__(self, f_type, f_name, f_params, f_body):
        self.f_type = f_type
        self.f_name = f_name
        self.f_params = f_params
        self.f_body = f_body

class Type_node(AST):
    def __init__(self, type):
        self.type = type

class Variable(AST):
    def __init__(self, variable):
        self.variable = variable

class Var_Decl(AST):
    def __init__(self, type_node, var_node):
        self.type_node = type_node
        self.var_node = var_node

class Assign(AST):
    def __init__(self, var_node, value):
        self.var_node = var_node
        self.value = value

class Body(AST):
    def __init__(self, stmts):
        self.stmts = stmts

class If_Stmt(AST):
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = else_body

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return '{} {} {}'.format(str(self.left), str(self.op), str(self.right))

class UnOp(AST):
    def __init__(self, op, node):
        self.op = op
        self.node = node

class Num(AST):
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)