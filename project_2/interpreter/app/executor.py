from app.nodes import *

vars = {}
funs = {}

class Var:
    def __init__(self, tip, naziv):
        self.tip = tip
        self.naziv = naziv
        self.vrednost = None

class Fun:
    def __init__(self, tip, naziv, vars, sadrzaj):
        self.tip = tip
        self.naziv = naziv
        self.vars = vars
        self.sadrzaj = sadrzaj

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
                    if isinstance(cvor, Postojanje):
                        self.visit(cvor)
                
                for cvor in node.cvorovi:
                    if isinstance(cvor, Dodela):
                        self.visit(cvor)

                for cvor in node.cvorovi:
                    if isinstance(cvor, Rutina):
                        self.visit(cvor)
            
                for cvor in node.cvorovi:
                    if(not isinstance(cvor, Postojanje)
                        and not isinstance(cvor, Dodela)
                        and not isinstance(cvor, Rutina)):
                        self.visit(cvor)
        
        def visit_Postojanje(self, node):
                naziv = self.visit(node.naziv)
                vars[naziv] = Var(node.tip, naziv)

        def visit_Dodela(self, node):
                izraz = self.visit(node.izraz)
                varijabla = self.visit(node.varijabla)
                vars[varijabla].vrednost = izraz

        def visit_Polje(self, node):
                tip = self.visit(node.tip)
                naziv = self.visit(node.naziv)

        def visit_Rutina(self, node):
                tip = None
                if node.tip is not None:
                    tip = self.visit(node.tip)
                naziv = self.visit(node.naziv)
                vars = {}
                for polje in node.polja.cvorovi:
                    polje_naziv = self.visit(polje.naziv)
                    vars[polje_naziv] = Var(polje.tip, polje_naziv)
                funs[naziv] = Fun(tip, naziv, vars, node.sadrzaj)
        
        def visit_Argumenti(self, node):
                argumenti = []
                for arg in node.argumenti:
                        if arg is not None:
                                argumenti.append(self.visit(arg))
                return argumenti

        def visit_RutinaPoziv(self, node):
                argumenti = self.visit(node.argumenti)
                naziv = self.visit(node.naziv)
                self.visit(funs[naziv].sadrzaj)

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
                            s += str(vars[arg.naziv].vrednost)
                        else:
                            s += str(self.visit(arg))
                    return s
                return None

        def visit_Vrati(self, node):
                return self.visit(node.izraz)

        def visit_PrekiniPonavljanje(self, node):
                pass
        
        def visit_NaredbaUslov(self, node):
                pitanje = self.visit(node.pitanje)
                if pitanje:
                    self.visit(node.da)
                else:
                    if node.ne != None:
                        self.visit(node.ne)

        def visit_NaredbaPonavljanje(self, node):
                pitanje = self.visit(node.pitanje)
                while pitanje:
                    self.visit(node.ponovi)

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
                    prvi = vars[prvi].vrednost

                if isinstance(node.drugi, Naziv):
                    drugi = vars[drugi].vrednost

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
                    if isinstance(node.prvi, CeoBroj) or isinstance(node.drugi, CeoBroj):
                        return float(prvi) == float(drugi)
                    elif isinstance(node.prvi, Struna) or isinstance(node.drugi, Struna):
                        return prvi == drugi
                    elif isinstance(node.prvi, JesteNije) or isinstance(node.drugi, JesteNije):
                        return prvi == drugi
                elif node.simbol == '!=':
                    return float(prvi) != float(drugi)
                elif node.simbol == '&&':
                    return prvi and drugi
                elif node.simbol == '||':
                    return prvi or drugi
                return None

        def visit_UnarnaOperacija(self, node):
                prvi = self.visit(node.prvi)

                if isinstance(node.prvi, Naziv):
                    prvi = vars[prvi].vrednost

                if node.simbol == '-':
                    return -prvi
                elif node.simbol == '!':
                    return not prvi
                return None

        def execute(self):
                tree = self.parser.program()
                self.visit(tree)
                return None
