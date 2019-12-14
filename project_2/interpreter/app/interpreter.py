import textwrap
from graphviz import Digraph

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, 'error_method')
        return visitor(node)

    def error_method(self, node):
        raise Exception("Nije nadjena metoda {}".format('visit_' + type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.ncount = 1
        self.dot = Digraph(comment='Nas program')
        self.dot.node_attr['shape']='box'
        self.dot.node_attr['fontsize'] = '12'
        self.dot.node_attr['height'] = '.1'
        self.dot.node_attr['ranksep'] = '.3'
        self.dot.edge_attr['arrowsize']='.5'


    def visit_Program(self, node):
        self.dot.node('node{}'.format(self.ncount), 'Program')
        node._num = self.ncount
        self.ncount += 1

        child_nodes = node.child_nodes

        for child in child_nodes:
            self.visit(child)
            self.dot.edge('node{}'.format(node._num), 'node{}'.format(child._num))

    def visit_Fun_Decl(self, node):
        self.dot.node('node{}'.format(self.ncount), 'Fun_Decl: {}'.format(node.f_name))
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.f_type)
        self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.f_type._num))

        # visit parameters

        self.visit(node.f_body)
        self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.f_body._num))

    def visit_Type_node(self, node):
        self.dot.node('node{}'.format(self.ncount), 'Type: {}'.format(node.type))
        node._num = self.ncount
        self.ncount += 1

    def visit_Variable(self, node):
        self.dot.node('node{}'.format(self.ncount), 'Variable: {}'.format(node.variable))
        node._num = self.ncount
        self.ncount += 1

    def visit_Var_Decl(self, node):
        self.dot.node('node{}'.format(self.ncount), 'Var_Decl')
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.type_node)
        self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.type_node._num))

        self.visit(node.var_node)
        self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.var_node._num))

    def visit_Assign(self, node):
        self.dot.node('node{}'.format(self.ncount), 'Assign')
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.var_node)
        self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.var_node._num))

        self.visit(node.value)
        self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.value._num))

    def visit_If_Stmt(self, node):
        self.dot.node('node{}'.format(self.ncount), 'IF')
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.condition)
        self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.condition._num))

        self.visit(node.body)
        self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.body._num))

        if  node.else_body != None:
            self.visit(node.else_body)
            self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.else_body._num))

    def visit_Body(self, node):
        self.dot.node('node{}'.format(self.ncount), 'Body')
        node._num = self.ncount
        self.ncount += 1

        stmts = node.stmts

        for stmt in stmts:
            self.visit(stmt)
            self.dot.edge('node{}'.format(node._num), 'node{}'.format(stmt._num))

    def visit_BinOp(self, node):
        self.dot.node('node{}'.format(self.ncount), '{}'.format(node.op))
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.left)
        self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.left._num))

        self.visit(node.right)
        self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.right._num))



    def visit_UnOp(self, node):
        self.dot.node('node{}'.format(self.ncount), '{}'.format(node.op))
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.node)
        self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.node._num))

    def visit_Num(self, node):
        self.dot.node('node{}'.format(self.ncount), '{}'.format(node.num))
        node._num = self.ncount
        self.ncount += 1

    def parse(self):
        tree = self.parser.program()
        self.visit(tree)
        return self.dot.source
