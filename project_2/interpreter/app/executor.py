from app.nodes import *

vars = {}
funs = {}
call_stack = []

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
                if len(call_stack) == 0:
                    vars[naziv] = Var(node.tip, naziv)
                else:
                    call_stack[-1].vars[naziv] = Var(node.tip, naziv)

        def visit_Dodela(self, node):
                izraz = self.visit(node.izraz)
                varijabla = self.visit(node.varijabla)
                self.set_var(varijabla, izraz)

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
                for arg in argumenti:
                    funs[naziv].vars[arg].vrednost = vars[arg].vrednost
                call_stack.append(funs[naziv])
                vrednost = self.visit(funs[naziv].sadrzaj)
                call_stack.pop()
                for arg in argumenti:
                    funs[naziv].vars[arg].vrednost = None
                return vrednost

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
                izraz = self.visit(node.izraz)
                if isinstance(node.izraz, Naziv):
                    izraz = call_stack[-1].vars[izraz].vrednost
                return izraz

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
                pitanje = True
                while pitanje:
                    pitanje = self.visit(node.pitanje)
                    for cvor in node.ponovi.cvorovi:
                        self.visit(cvor)
                        if isinstance(node, PrekiniPonavljanje):
                            return

        def visit_CelinaCelina(self, node):
                for cvor in node.cvorovi:
                        if isinstance(cvor, Vrati):
                            return self.visit(cvor)
                        self.visit(cvor)
                return None

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
                    prvi = self.get_var(prvi)

                if isinstance(node.drugi, Naziv):
                    drugi = self.get_var(drugi)

                if node.simbol == '+':
                    return int(prvi) + int(drugi)
                elif node.simbol == '-':
                    return int(prvi) - int(drugi)
                elif node.simbol == '*':
                    return int(prvi) * int(drugi)
                elif node.simbol == '/':
                    return int(prvi) / int(drugi)
                elif node.simbol == '%':
                    return int(prvi) % int(drugi)
                elif node.simbol == '<':
                    return int(prvi) < int(drugi)
                elif node.simbol == '>':
                    return int(prvi) > int(drugi)
                elif node.simbol == '<=':
                    return int(prvi) >= int(drugi)
                elif node.simbol == '>=':
                    return int(prvi) <= int(drugi)
                elif node.simbol == '=':
                    if isinstance(node.prvi, CeoBroj) or isinstance(node.drugi, CeoBroj):
                        return int(prvi) == int(drugi)
                    elif isinstance(node.prvi, Struna) or isinstance(node.drugi, Struna):
                        return prvi == drugi
                    elif isinstance(node.prvi, JesteNije) or isinstance(node.drugi, JesteNije):
                        return prvi == drugi
                elif node.simbol == '!=':
                    return int(prvi) != int(drugi)
                elif node.simbol == '&&':
                    return prvi and drugi
                elif node.simbol == '||':
                    return prvi or drugi
                return None

        def visit_UnarnaOperacija(self, node):
                prvi = self.visit(node.prvi)

                if isinstance(node.prvi, Naziv):
                    prvi = self.get_var(prvi)

                if node.simbol == '-':
                    return -prvi
                elif node.simbol == '!':
                    return not prvi
                return None

        def get_var(self, naziv):
            if len(call_stack) == 0:
                return vars[naziv].vrednost
            else:
                return call_stack[-1].vars[naziv].vrednost

        def set_var(self, naziv, vrednost):
            if len(call_stack) == 0:
                vars[naziv].vrednost = vrednost
            else:
                call_stack[-1].vars[naziv].vrednost = vrednost

        def log_vars(self):
            print("*** GLOBAL SCOPE ***")
            for (naziv, var) in vars.items():
                print("{} {}={}".format(var.tip.tip, var.naziv, var.vrednost))
            print("*** CALL STACK *** ")
            for fun in call_stack:
                for (naziv, var) in fun.vars.items():
                    print("{} {}={}".format(var.tip.tip, var.naziv, var.vrednost))
            print("---------- * ----------")

        def execute(self):
                tree = self.parser.program()
                self.visit(tree)
                return None
