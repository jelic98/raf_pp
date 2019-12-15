from app.type import *
from app.nodes import *
from functools import wraps
import pickle

class Parser():
        def __init__(self, lexer):
                self.lexer = lexer
                self.current_token = self.lexer.get_next_token()

        def restorable(fn):
                @wraps(fn)
                def wrapper(self, *args, **kwargs):
                        state = pickle.dumps(self.__dict__)
                        result = fn(self, *args, **kwargs)
                        self.__dict__ = pickle.loads(state)
                        return result
                return wrapper

        def type_error(self, expected, found):
                self.error("Expected: {}, Found: {}".format(expected, found))

        def error(self, text):
                raise Exception(text)

        def eat(self, token_type):
                if self.current_token.token_type == token_type:
                        self.current_token = self.lexer.get_next_token()
                else:
                        self.type_error(token_type, self.current_token.token_type)
        
        def program(self):
                cvorovi = []
                while self.current_token.token_type not in [EOF, PROGRAM_KRAJ]:
                        if self.current_token.token_type == POSTOJANJE_POCETAK:
                                cvorovi.append(self.postojanje())
                        elif self.current_token.token_type == DODELA_POCETAK:
                                cvorovi.append(self.dodela())
                        elif self.current_token.token_type == NAREDBA_POCETAK:
                                cvorovi.append(self.naredba())
                        elif self.current_token.token_type == RUTINA_POCETAK:
                                cvorovi.append(self.rutina())
                        else:
                                self.error('Derivation error: PROGRAM')
                return Program(cvorovi)

        def naredba(self):
                if self.is_naredba_uslov():
                        return self.naredba_uslov()
                elif self.current_token.token_type == NAREDBA_PONAVLJANJE:
                        return self.vnaredba_ponavljanje()
                else:
                        self.error('Derivation error: NAREDBA')
        
        def debug(self):
                print("{} {}".format(self.current_token.token_type, self.current_token.value))

        @restorable
        def is_naredba_uslov(self):
                self.eat(NAREDBA_POCETAK)
                self.celina_da()
                self.celina_ne()
                self.celina_pitanje()
                self.eat(NAREDBA_KRAJ)
                self.eat(COLON)
                return self.current_token.token_type == NAREDBA_USLOV

        def naredba_uslov(self):
                self.eat(NAREDBA_POCETAK)
                pitanje = None
                da = None
                ne = None
                if self.is_celina_da():
                        da = self.celina_da()
                if self.is_celina_ne():
                        ne = self.celina_ne()
                if self.is_celina_pitanje():
                        pitanje = self.celina_pitanje()
                self.eat(NAREDBA_KRAJ)
                self.eat(COLON)
                self.eat(NAREDBA_USLOV)
                return NaredbaUslov(pitanje, da, ne)

        def naredba_ponavljanje(self):
                self.eat(NAREDBA_POCETAK)
                pitanje = None
                ponovi = None
                if self.is_celina_pitanje():
                        self.eat(CELINA_PITANJE)
                        pitanje = self.celina_pitanje()
                if self.current_token.token_type == CELINA_PONOVI:
                        self.eat(CELINA_PONOVI)
                        ponovi = self.celina_ponovi()
                self.eat(NAREDBA_KRAJ)
                self.eat(COLON)
                self.eat(NAREDBA_PONAVLJANJE)
                return NaredbaUslov(pitanje, ponovi)

        def var_declaration_list(self):
                declarations = []
                type_node = Type_node(self.current_token.value)
                self.eat(TIP_PODATKA)
                var_node = Variable(self.current_token.value)
                self.eat(NAZIV)
                declarations.extend(self.var_declaration(type_node, var_node))
                while self.current_token.token_type == COMMA:
                        self.eat(COMMA)
                        var_node = Variable(self.current_token.value)
                        self.eat(NAZIV)
                        declarations.extend(self.var_declaration(type_node, var_node))
                self.eat(SEMICOLON)
                return declarations

        def dodela(self):
                self.eat(DODELA_POCETAK)
                self.eat(PIPE)
                izraz = self.logic()
                self.eat(PIPE)
                varijabla = self.naziv()
                self.eat(DODELA_KRAJ)
                return Dodela(izraz, varijabla)

        def postojanje(self):
                self.eat(POSTOJANJE_POCETAK)
                self.eat(PIPE)
                tip = self.tip_podatka()
                self.eat(PIPE)
                naziv = self.naziv()
                self.eat(POSTOJANJE_KRAJ)
                return Postojanje(tip, naziv)

        def polje(self):
                self.eat(POLJE_POCETAK)
                self.eat(PIPE)
                tip = self.tip_podatka()
                self.eat(PIPE)
                naziv = self.naziv()
                self.eat(POLJE_KRAJ)
                return Polje(tip, naziv)

        @restorable
        def is_celina_pitanje(self):
                self.eat(CELINA_POCETAK)
                while self.current_token.token_type != CELINA_KRAJ:
                    self.eat(self.current_token.token_type)
                self.eat(CELINA_KRAJ)
                self.eat(COLON)
                return self.current_token.token_type == CELINA_PITANJE

        def celina_pitanje(self):
                self.eat(CELINA_POCETAK)
                izraz = self.logic()
                self.eat(CELINA_KRAJ)
                self.eat(COLON)
                self.eat(CELINA_PITANJE)
                return CelinaPitanje(izraz)

        @restorable
        def is_celina_da(self):
                self.eat(CELINA_POCETAK)
                while self.current_token.token_type != CELINA_KRAJ:
                    self.eat(self.current_token.token_type)
                self.eat(CELINA_KRAJ)
                self.eat(COLON)
                return self.current_token.token_type == CELINA_DA

        def celina_da(self):
                self.eat(CELINA_POCETAK)
                celina = self.celina_celina()
                self.eat(CELINA_KRAJ)
                self.eat(COLON)
                self.eat(CELINA_DA)
                return CelinaDa(celina)

        @restorable
        def is_celina_ne(self):
                self.eat(CELINA_POCETAK)
                while self.current_token.token_type != CELINA_KRAJ:
                    self.eat(self.current_token.token_type)
                self.eat(CELINA_KRAJ)
                self.eat(COLON)
                return self.current_token.token_type == CELINA_NE

        def celina_ne(self):
                self.eat(CELINA_POCETAK)
                celina = self.celina_celina()
                self.eat(CELINA_KRAJ)
                self.eat(COLON)
                self.eat(CELINA_NE)
                return CelinaNe(celina)

        def celina_ponovi(self):
                self.eat(CELINA_POCETAK)
                celina = self.celina_celina()
                self.eat(CELINA_KRAJ)
                self.eat(COLON)
                self.eat(CELINA_PONOVI)
                return CelinaPonovi(celina)

        def celina_polje(self):
                self.eat(CELINA_POCETAK)
                polja = self.polje()
                self.eat(CELINA_KRAJ)
                self.eat(COLON)
                self.eat(CELINA_POLJE)
                return CelinaPolje(celina)

        def celina_celina(self):
                cvorovi = []
                while self.current_token.token_type != CELINA_KRAJ:
                        if self.current_token.token_type == POSTOJANJE_POCETAK:
                                cvorovi.append(self.postojanje())
                        elif self.current_token.token_type == DODELA_POCETAK:
                                cvorovi.append(self.dodela())
                        elif self.current_token.token_type == NAREDBA_POCETAK:
                                cvorovi.append(self.naredba())
                        elif self.current_token.token_type == RUTINA_POZIV_POCETAK:
                                cvorovi.append(self.rutina_poziv())
                        elif self.current_token.token_type == UGRADJENA_RUTINA_POZIV_POCETAK:
                                cvorovi.append(self.ugradjena_rutina_poziv())
                        else:
                            self.error('Derivation error: CELINA_CELINA')
                return CelinaCelina(cvorovi)

        def ugradjena_rutina_poziv(self):
            self.eat(UGRADJENA_RUTINA_POZIV_POCETAK)
            self.eat(PIPE)
            argumenti = []
            while self.current_token.token_type != UGRADJENA_RUTINA_POZIV_KRAJ:
                argumenti.append(self.logic())
                if self.current_token.token_type == STRUNA:
                    self.eat(STRUNA)
                if self.current_token.token_type == COMMA:
                    self.eat(COMMA)
            self.eat(UGRADJENA_RUTINA_POZIV_KRAJ)
            self.eat(COLON)
            naziv = self.naziv()
            return UgradjenaRutinaPoziv(argumenti, naziv)

        def tip_podatka(self):
                if self.current_token.token_type == TIP_PODATKA:
                        tip = TipPodatka(self.current_token.value)
                        self.eat(TIP_PODATKA)
                        return tip
                else:
                    self.error('Derivation error: TIP_PODATKA')

        def naziv(self):
                if self.current_token.token_type == NAZIV:
                        naziv = Naziv(self.current_token.value)
                        self.eat(NAZIV)
                        return naziv
                else:
                    self.error('Derivation error: NAZIV')

        def factor(self):
                token = self.current_token
                if token.token_type == CEO_BROJ:
                        self.eat(CEO_BROJ)
                        return CeoBroj(token.value)
                elif token.token_type == NAZIV:
                        self.eat(NAZIV)
                        return Naziv(token.value)
                elif token.token_type in [MINUS, LOGICKO_NE]:
                        op_token = self.current_token
                        if op_token.token_type == MINUS:
                                self.eat(MINUS)
                        elif op_token.token_type == LOGICKO_NE:
                                self.eat(LOGICKO_NE)
                        result = None
                        if self.current_token.token_type == ZAGRADA_OTVORENA:
                                self.eat(ZAGRADA_OTVORENA)
                                result = self.logic()
                                self.eat(ZAGRADA_ZATVORENA)
                        else:
                                result = self.factor()
                        if op_token.token_type == LOGICKO_NE:
                                self.check_logic(result)
                        return UnarnaOperacija(op_token.value, result)
                elif token.token_type == ZAGRADA_OTVORENA:
                        self.eat(ZAGRADA_OTVORENA)
                        result = self.logic()
                        self.eat(ZAGRADA_ZATVORENA)
                        return result
                elif token.token_type == RUTINA_POZIV_POCETAK:
                        return rutina_poziv()
                elif token.token_type == UGRADJENA_RUTINA_POZIV_POCETAK:
                        return self.ugradjena_rutina_poziv()

        def term(self):
                left_node = self.factor()
                while self.current_token.token_type in [MNOZENJE, DELJENJE, OSTATAK]:
                        if self.current_token.token_type == MNOZENJE:
                                self.eat(MNOZENJE)
                                right_node = self.factor()
                                left_node = BinarnaOperacija(left_node, '*', right_node)
                        elif self.current_token.token_type == DELJENJE:
                                self.eat(DELJENJE)
                                right_node = self.factor()
                                left_node = BinarnaOperacija(left_node, '/', right_node)
                        elif self.current_token.token_type == OSTATAK:
                                self.eat(OSTATAK)
                                right_node = self.factor()
                                left_node = BinarnaOperacija(left_node, '%', right_node)
                return left_node

        def expr(self):
                left_node = self.term()
                while self.current_token.token_type in [PLUS, MINUS]:
                        if self.current_token.token_type == PLUS:
                                self.eat(PLUS)
                                right_node = self.term()
                                left_node = BinarnaOperacija(left_node, '+', right_node)
                        elif self.current_token.token_type == MINUS:
                                self.eat(MINUS)
                                right_node = self.term()
                                left_node = BinarnaOperacija(left_node, '-', right_node)
                return left_node

        def compare(self):
                left_node = self.expr()
                if self.current_token.token_type == VECE:
                        self.eat(VECE)
                        right_node = self.expr()
                        left_node = BinarnaOperacija(left_node, '>', right_node)
                elif self.current_token.token_type == MANJE:
                        self.eat(MANJE)
                        right_node = self.expr()
                        left_node = BinarnaOperacija(left_node, '<', right_node)
                elif self.current_token.token_type == VECE_JEDNAKO:
                        self.eat(VECE_JEDNAKO)
                        right_node = self.expr()
                        left_node = BinarnaOperacija(left_node, '>=', right_node)
                elif self.current_token.token_type == MANJE_JEDNAKO:
                        self.eat(MANJE_JEDNAKO)
                        right_node = self.expr()
                        left_node = BinarnaOperacija(left_node, '<=', right_node)
                elif self.current_token.token_type == JEDNAKO:
                        self.eat(JEDNAKO)
                        right_node = self.expr()
                        left_node = BinarnaOperacija(left_node, '=', right_node)
                elif self.current_token.token_type == NIJE_JEDNAKO:
                        self.eat(NIJE_JEDNAKO)
                        right_node = self.expr()
                        left_node = BinarnaOperacija(left_node, '!=', right_node)
                return left_node

        def check_logic(self, node):
                if str(type(node).__name__) == 'BinarnaOperacija':
                        if node.simbol not in ['<', '>', '>=', '<=', '=', '!=']:
                                self.type_error('logical operator ', node.simbol)
                elif str(type(node).__name__) == 'UnarnaOperacija':
                        if node.simbol not in ['!']:
                                self.type_error('not', node.simbol)
                else:
                    self.error('Derivation error: LOGIC')

        def logic(self):
                left_node = self.compare()
                if self.current_token.token_type == LOGICKO_I:
                        self.eat(LOGICKO_I)
                        self.check_logic(left_node)
                        right_node = self.compare()
                        self.check_logic(right_node)
                        left_node = BinarnaOperacija(left_node, 'and', right_node)
                elif self.current_token.token_type == LOGICKO_ILI:
                        self.eat(LOGICKO_ILI)
                        self.check_logic(left_node)
                        right_node = self.compare()
                        self.check_logic(right_node)
                        left_node = BinarnaOperacija(left_node, 'or', right_node)
                return left_node
