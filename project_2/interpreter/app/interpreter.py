import textwrap
from graphviz import Digraph

class NodeVisitor(object):
        def visit(self, node):
                method_name = 'visit_' + type(node).__name__
                visitor = getattr(self, method_name, 'error_method')
                print(method_name)
                return visitor(node)

        def error_method(self, node):
                raise Exception("Method missing: {}".format('visit_' + type(node).__name__))

class Interpreter(NodeVisitor):
        def __init__(self, parser):
                self.parser = parser
                self.ncount = 1
                self.dot = Digraph(comment='RafLang AST')
                self.dot.node_attr['shape']='box'
                self.dot.node_attr['fontsize'] = '12'
                self.dot.node_attr['height'] = '.1'
                self.dot.node_attr['ranksep'] = '.3'
                self.dot.edge_attr['arrowsize']='.5'

        def visit_Program(self, node):
                self.dot.node('node{}'.format(self.ncount), 'PROGRAM')
                node._num = self.ncount
                self.ncount += 1

                for cvor in node.cvorovi:
                        self.visit(cvor)
                        self.dot.edge('node{}'.format(node._num), 'node{}'.format(cvor._num))
        
        def visit_Postojanje(self, node):
                self.dot.node('node{}'.format(self.ncount), 'POSTOJANJE')
                node._num = self.ncount
                self.ncount += 1

                self.visit(node.tip)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.tip._num))

                self.visit(node.naziv)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.naziv._num))

        def visit_Dodela(self, node):
                self.dot.node('node{}'.format(self.ncount), 'DODELA')
                node._num = self.ncount
                self.ncount += 1

                self.visit(node.izraz)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.izraz._num))

                self.visit(node.varijabla)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.varijabla._num))

        def visit_Polje(self, node):
                self.dot.node('node{}'.format(self.ncount), 'POLJE')
                node._num = self.ncount
                self.ncount += 1

                self.visit(node.tip)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.tip._num))

                self.visit(node.naziv)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.naziv._num))

        def visit_Rutina(self, node):
                self.dot.node('node{}'.format(self.ncount), 'RUTINA')
                node._num = self.ncount
                self.ncount += 1

                self.visit(node.tip)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.tip._num))

                self.visit(node.sadrzaj)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.sadrzaj._num))

                self.visit(node.naziv)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.naziv._num))

        def visit_RutinaPoziv(self, node):
                self.dot.node('node{}'.format(self.ncount), 'RUTINA_POZIV')
                node._num = self.ncount
                self.ncount += 1

                for arg in node.arguenti:
                        self.visit(arg)
                        self.dot.edge('node{}'.format(node._num), 'node{}'.format(arg._num))
        
                node._num = self.ncount
                self.ncount += 1

                self.visit(node.naziv)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.naziv._num))

        def visit_UgradjenaRutinaPoziv(self, node):
                self.dot.node('node{}'.format(self.ncount), 'UGRADJENA_RUTINA_POZIV')
                node._num = self.ncount
                self.ncount += 1

                for arg in node.argumenti:
                        if arg is not None:
                                self.visit(arg)
                                self.dot.edge('node{}'.format(node._num), 'node{}'.format(arg._num))
        
                self.visit(node.naziv)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.naziv._num))

        def visit_Vrati(self, node):
                self.dot.node('node{}'.format(self.ncount), 'VRATI')
                node._num = self.ncount
                self.ncount += 1

                self.visit(node.izraz)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.izraz._num))

        def visit_NaredbaUslov(self, node):
                self.dot.node('node{}'.format(self.ncount), 'NAREDBA_USLOV')
                node._num = self.ncount
                self.ncount += 1

                self.visit(node.pitanje)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.pitanje._num))

                self.visit(node.da)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.da._num))

                if node.ne != None:
                        self.visit(node.ne)
                        self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.ne._num))

        def visit_NaredbaPonavljanje(self, node):
                self.dot.node('node{}'.format(self.ncount), 'NAREDBA_PONAVLJANJE')
                node._num = self.ncount
                self.ncount += 1

                self.visit(node.pitanje)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.pitanje._num))

                self.visit(node.ponovi)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.ponovi._num))

        def visit_CelinaCelina(self, node):
                self.dot.node('node{}'.format(self.ncount), 'CELINA')
                node._num = self.ncount
                self.ncount += 1

                for cvor in node.cvorovi:
                        self.visit(cvor)
                        self.dot.edge('node{}'.format(node._num), 'node{}'.format(cvor._num))

        def visit_CeoBroj(self, node):
                self.dot.node('node{}'.format(self.ncount), '{}'.format(node.broj))
                node._num = self.ncount
                self.ncount += 1

        def visit_Struna(self, node):
                self.dot.node('node{}'.format(self.ncount), '{}'.format(node.struna))
                node._num = self.ncount
                self.ncount += 1

        def visit_TipPodatka(self, node):
                self.dot.node('node{}'.format(self.ncount), '{}'.format(node.tip))
                node._num = self.ncount
                self.ncount += 1

        def visit_Naziv(self, node):
                self.dot.node('node{}'.format(self.ncount), '{}'.format(node.naziv))
                node._num = self.ncount
                self.ncount += 1

        def visit_BinarnaOperacija(self, node):
                self.dot.node('node{}'.format(self.ncount), '{}'.format(node.simbol))
                node._num = self.ncount
                self.ncount += 1
                
                self.visit(node.prvi)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.prvi._num))

                self.visit(node.drugi)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.drugi._num))

        def visit_UnarnaOperacija(self, node):
                self.dot.node('node{}'.format(self.ncount), '{}'.format(node.simbol))
                node._num = self.ncount
                self.ncount += 1

                self.visit(node.prvi)
                self.dot.edge('node{}'.format(node._num), 'node{}'.format(node.prvi._num))

        def parse(self):
                tree = self.parser.program()
                self.visit(tree)
                return self.dot.source
