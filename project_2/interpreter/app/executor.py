from app.nodes import *

vars = []

class Var:
    def __init__(self, type, name, value):
        self.type = type
        self.name = name
        self.value = value

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
                tip = self.visit(node.tip)
                naziv = self.visit(node.naziv)
                vars.append(Var(tip, naziv, None))

        def visit_Dodela(self, node):
                izraz = self.visit(node.izraz)
                varijabla = self.visit(node.varijabla)

                for var in vars:
                    if var.name == varijabla:
                        var.value = izraz
                        break

        def visit_Polje(self, node):
                tip = self.visit(node.tip)
                naziv = self.visit(node.naziv)

        def visit_Rutina(self, node):
                if node.tip is not None:
                    tip = self.visit(node.tip)

                sadrzaj = self.visit(node.sadrzaj)
                naziv = self.visit(node.naziv)

        def visit_Argumenti(self, node):
                argumenti = []
                for arg in node.argumenti:
                        if arg is not None:
                                argumenti.append(self.visit(arg))
                return argumenti

        def visit_RutinaPoziv(self, node):
                argumenti = self.visit(node.argumenti)
                naziv = self.visit(node.naziv)

        def visit_UgradjenaRutinaPoziv(self, node):
                argumenti = self.visit(node.argumenti)
                naziv = self.visit(node.naziv)
                if naziv == "ucitaj":
                    return input()
                elif naziv == "ispisi":
                    print(argumenti[0])
                elif naziv == "spoji_strune":
                    s = ""
                    for arg in node.argumenti.argumenti:
                        if isinstance(arg, Naziv):
                            for var in vars:
                                if var.name == arg.naziv:
                                    s += str(var.value)
                                    break
                        else:
                            s += str(self.visit(arg))
                    return s
                return None

        def visit_Vrati(self, node):
                izraz = self.visit(node.izraz)

        def visit_PrekiniPonavljanje(self, node):
                pass
        
        def visit_NaredbaUslov(self, node):
                pitanje = self.visit(node.pitanje)

                if pitanje:
                    da = self.visit(node.da)
                else:
                    if node.ne != None:
                        ne = self.visit(node.ne)

        def visit_NaredbaPonavljanje(self, node):
                pitanje = self.visit(node.pitanje)
                ponovi = self.visit(node.ponovi)

        def visit_CelinaCelina(self, node):
                for cvor in node.cvorovi:
                        self.visit(cvor)

        def visit_CeoBroj(self, node):
                return node.broj

        def visit_Struna(self, node):
                return node.struna

        def visit_JesteNije(self, node):
                return node.jestenije

        def visit_TipPodatka(self, node):
                return node.tip

        def visit_Naziv(self, node):
                return node.naziv

        def visit_ElementNiza(self, node):
                self.visit(node.naziv)

                for indeks in node.indeksi:
                        if indeks is not None:
                                self.visit(indeks)

        def visit_BinarnaOperacija(self, node):
                prvi = self.visit(node.prvi)
                drugi = self.visit(node.drugi)
               
                if isinstance(node.prvi, Naziv):
                    for var in vars:
                        if var.name == prvi:
                            prvi = var.value
                            break

                if isinstance(node.drugi, Naziv):
                    for var in vars:
                        if var.name == drugi:
                            drugi = var.value
                            break

                if node.simbol == '+':
                    return float(prvi) + float(drugi)
                elif node.simbol == '-':
                    return float(prvi) - float(drugi)
                elif node.simbol == '*':
                    return float(prvi) * float(drugi)
                elif node.simbol == '/':
                    return float(prvi) / float(drugi)
                elif node.simbol == '%':
                    return int(prvi) % int(drugi)
                elif node.simbol == '<':
                    return float(prvi) < float(drugi)
                elif node.simbol == '>':
                    return float(prvi) > float(drugi)
                elif node.simbol == '<=':
                    return float(prvi) >= float(drugi)
                elif node.simbol == '>=':
                    return float(prvi) <= float(drugi)
                elif node.simbol == '=':
                    return float(prvi) == float(drugi)
                return None

        def visit_UnarnaOperacija(self, node):
                self.visit(node.prvi)

        def execute(self):
                tree = self.parser.program()
                self.visit(tree)
                return None
