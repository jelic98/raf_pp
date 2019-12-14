class AST(object):
        pass

class CeoBroj(AST):
        def __init__(self, broj):
                self.broj = broj

class Struna(AST):
        def __init__(self, struna):
                self.struna = struna

class BinarnaOperacija(AST):
        def __init__(self, prvi, simbol, drugi):
                self.prvi = prvi
                self.simbol = simbol
                self.drugi = drugi

class UnarnaOperacija(AST):
        def __init__(self, simbol, prvi):
                self.simbol = simbol
                self.prvi = node

class Program(AST):
        def __init__(self, cvorovi):
                self.cvorovi = cvorovi

class Postojanje(AST):
        def __init__(self, tip, naziv):
            self.tip = tip
            self.naziv = naziv
