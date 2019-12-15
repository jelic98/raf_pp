class AST(object):
        pass

class Program(AST):
        def __init__(self, cvorovi):
                self.cvorovi = cvorovi

class Postojanje(AST):
        def __init__(self, tip, naziv):
                self.tip = tip
                self.naziv = naziv

class Dodela(AST):
        def __init__(self, izraz, varijabla):
                self.izraz = izraz
                self.varijabla = varijabla

class Polje(AST):
        def __init__(self, tip, naziv):
                self.tip = tip
                self.naziv = naziv

class Rutina(AST):
        def __init__(self, tip, sadrzaj, naziv):
                self.tip = tip
                self.sadrzaj = sadrzaj
                self.naziv = naziv

class RutinaPoziv(AST):
        def __init__(self, argumenti, naziv):
                self.argumenti = argumenti
                self.naziv = naziv

class UgradjenaRutinaPoziv(AST):
        def __init__(self, argumenti, naziv):
                self.argumenti = argumenti
                self.naziv = naziv

class Vrati(AST):
        def __init__(self, izraz):
                self.izraz = izraz

class NaredbaUslov(AST):
        def __init__(self, pitanje, da, ne):
                self.pitanje = pitanje
                self.da = da
                self.ne = ne

class NaredbaPonavljanje(AST):
        def __init__(self, pitanje, ponovi):
                self.pitanje = pitanje
                self.ponovi = ponovi

class CelinaCelina(AST):
        def __init__(self, cvorovi):
                self.cvorovi = cvorovi

class CeoBroj(AST):
        def __init__(self, broj):
                self.broj = broj

class TipPodatka(AST):
        def __init__(self, tip):
                self.tip = tip

class Struna(AST):
        def __init__(self, struna):
                self.struna = struna

class Naziv(AST):
        def __init__(self, naziv):
                self.naziv = naziv

class BinarnaOperacija(AST):
        def __init__(self, prvi, simbol, drugi):
                self.prvi = prvi
                self.simbol = simbol
                self.drugi = drugi

class UnarnaOperacija(AST):
        def __init__(self, simbol, prvi):
                self.simbol = simbol
                self.prvi = node
