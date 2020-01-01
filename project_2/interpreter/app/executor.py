from app.type import *
from app.nodes import *

vars = {}
funs = {}
call_stack = []
types = {
    CEO_BROJ: "~ceo_broj",
    STRUNA: "~struna",
    JESTE_NIJE: "~jeste_nije"
}

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
                self.add_var(node.tip, node.naziv.naziv)

        def visit_Dodela(self, node):
                izraz = self.visit(node.izraz)
                varijabla = node.varijabla
                if isinstance(varijabla, Naziv):
                    self.set_var(izraz, varijabla.naziv)
                elif isinstance(varijabla, ElementNiza):
                    self.set_var(izraz, varijabla.naziv.naziv, varijabla.indeksi)

        def visit_Polje(self, node):
                tip = self.visit(node.tip)
                naziv = self.visit(node.naziv)

        def visit_Rutina(self, node):
                tip = None
                if node.tip is not None:
                    tip = self.visit(node.tip)
                naziv = node.naziv.naziv
                vars = {}
                for polje in node.polja.cvorovi:
                    polje_naziv = polje.naziv.naziv
                    vars[polje_naziv] = Var(polje.tip, polje_naziv)
                funs[naziv] = Fun(tip, naziv, vars, node.sadrzaj)
        
        def visit_Argumenti(self, node):
            argumenti = []
            for arg in node.argumenti:
                if isinstance(arg, Naziv):
                    argumenti.append(arg.naziv)
                else:
                    argumenti.append(self.visit(arg))
            return argumenti

        def visit_RutinaPoziv(self, node):
                argumenti = self.visit(node.argumenti)
                naziv = node.naziv.naziv
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
                naziv = node.naziv.naziv
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
                izraz = node.izraz
                if isinstance(izraz, Naziv):
                    izraz = call_stack[-1].vars[izraz.naziv].vrednost
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
                pitanje = self.visit(node.pitanje)
                while pitanje:
                    for cvor in node.ponovi.cvorovi:
                        self.visit(cvor)
                        if isinstance(node, PrekiniPonavljanje):
                            return
                    pitanje = self.visit(node.pitanje)

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
                return self.get_var(node.naziv).vrednost

        def visit_ElementNiza(self, node):
                vrednost = self.visit(node.naziv)
                for indeks in node.indeksi:
                        if indeks is not None:
                                if isinstance(indeks, Naziv):
                                        indeks = int(self.get_var(indeks.naziv).vrednost)
                                else:
                                        indeks = int(self.visit(indeks))
                                vrednost = vrednost[indeks]
                return vrednost

        def visit_BinarnaOperacija(self, node):
                prvi = self.visit(node.prvi)
                drugi = self.visit(node.drugi)
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
                if node.simbol == '-':
                    return -prvi
                elif node.simbol == '!':
                    return not prvi
                return None

        def add_var(self, tip, naziv):
            if len(call_stack) > 0 and naziv not in call_stack[-1].vars:
                call_stack[-1].vars[naziv] = Var(tip, naziv)
            elif len(call_stack) == 0 and naziv not in vars:
                vars[naziv] = Var(tip, naziv)
                if tip.tip == types[STRUNA]:
                    self.set_var([], naziv)

        def get_var(self, naziv):
            if len(call_stack) > 0 and naziv in call_stack[-1].vars:
                return call_stack[-1].vars[naziv]
            else:
                return vars[naziv]

        def set_var(self, vrednost, naziv, indeksi=None):
            if len(call_stack) > 0 and naziv in call_stack[-1].vars:
                if indeksi is None:
                    call_stack[-1].vars[naziv].vrednost = vrednost
                else:
                    self.set_arr_var(vrednost, call_stack[-1].vars[naziv].vrednost, indeksi)
            else:
                if indeksi is None:
                    vars[naziv].vrednost = vrednost
                else:
                    self.set_arr_var(vrednost, vars[naziv].vrednost, indeksi)

        def set_arr_var(self, nova, niz, indeksi):
            prev_vrednost = None
            prev_indeks = None
            vrednost = niz
            for indeks in indeksi:
                if indeks is not None:
                    if isinstance(indeks, Naziv):
                        indeks = int(self.get_var(indeks.naziv).vrednost)
                    else:
                        indeks = int(self.visit(indeks))
                if indeks >= len(vrednost):
                    vrednost.append(None)
                prev_vrednost = vrednost
                prev_indeks = indeks
                vrednost = vrednost[indeks]
            prev_vrednost[prev_indeks] = nova

        def log_vars(self):
            print("*** GLOBAL SCOPE ***")
            for (naziv, var) in vars.items():
                print("{}->{} {}={}".format(naziv, var.tip.tip, var.naziv, var.vrednost))
            print("*** CALL STACK *** ")
            for fun in call_stack:
                for (naziv, var) in fun.vars.items():
                    print("{}->{} {}={}".format(naziv, var.tip.tip, var.naziv, var.vrednost))
            print("---------- * ----------")

        def execute(self):
                tree = self.parser.program()
                self.visit(tree)
                return None
