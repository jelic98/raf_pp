class NodeVisitor(object):
        def visit(self, node):
                method_name = 'visit_' + type(node).__name__
                visitor = getattr(self, method_name, 'error_method')
                return visitor(node)

        def error_method(self, node):
                raise Exception("Method missing: {}".format('visit_' + type(node).__name__))

class Executor(NodeVisitor):
        def __init__(self, parser):
                self.parser = parser

        def visit_Program(self, node):
                for cvor in node.cvorovi:
                        self.visit(cvor)
        
        def visit_Postojanje(self, node):
                self.visit(node.tip)
                self.visit(node.naziv)

        def visit_Dodela(self, node):
                self.visit(node.izraz)
                self.visit(node.varijabla)

        def visit_Polje(self, node):
                self.visit(node.tip)
                self.visit(node.naziv)

        def visit_Rutina(self, node):
                if node.tip is not None:
                    self.visit(node.tip)

                self.visit(node.sadrzaj)
                self.visit(node.naziv)

        def visit_Argumenti(self, node):
                for arg in node.argumenti:
                        if arg is not None:
                                self.visit(arg)

        def visit_RutinaPoziv(self, node):
                self.visit(node.argumenti)
                self.visit(node.naziv)

        def visit_UgradjenaRutinaPoziv(self, node):
                self.visit(node.argumenti)
                self.visit(node.naziv)

        def visit_Vrati(self, node):
                self.visit(node.izraz)

        def visit_PrekiniPonavljanje(self, node):
                pass
        
        def visit_NaredbaUslov(self, node):
                self.visit(node.pitanje)
                self.visit(node.da)

                if node.ne != None:
                        self.visit(node.ne)

        def visit_NaredbaPonavljanje(self, node):
                self.visit(node.pitanje)
                self.visit(node.ponovi)

        def visit_CelinaCelina(self, node):
                for cvor in node.cvorovi:
                        self.visit(cvor)

        def visit_CeoBroj(self, node):
                pass

        def visit_Struna(self, node):
                pass

        def visit_JesteNije(self, node):
                pass

        def visit_TipPodatka(self, node):
                pass

        def visit_Naziv(self, node):
                pass

        def visit_ElementNiza(self, node):
                self.visit(node.naziv)

                for indeks in node.indeksi:
                        if indeks is not None:
                                self.visit(indeks)

        def visit_BinarnaOperacija(self, node):
                self.visit(node.prvi)
                self.visit(node.drugi)

        def visit_UnarnaOperacija(self, node):
                self.visit(node.prvi)

        def execute(self):
                tree = self.parser.program()
                self.visit(tree)
                return None
