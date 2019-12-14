from app.type import *
from app.token import Token

class Lexer():
        def __init__(self, text):       
                self.text = text
                self.pos = 0

        def skip_whitespace(self):
                while self.pos < len(self.text) and self.text[self.pos].isspace():
                        self.pos += 1

        def parse_number(self):
                number = ''
                while(self.pos < len(self.text) and self.text[self.pos].isdigit()):
                        number += self.text[self.pos]
                        self.pos += 1
                self.pos -= 1
                return int(number)
        
        def parse_string(self):
            pass

        def parse_keyword(self):
                string = ''
                while(self.pos < len(self.text)
                    and (self.text[self.pos].isalpha()
                    or self.text[self.pos].isdigit()
                    or self.text[self.pos] == '_'
                    or self.text[self.pos] == '#'
                    or self.text[self.pos] == '~')):
                        string += self.text[self.pos]
                        self.pos += 1
                self.pos -= 1
                if string == '#program':
                        return Token(PROGRAM_POCETAK, True)
                elif string == '##program':
                        return Token(PROGRAM_KRAJ, True)
                elif string == '#postojanje':
                        return Token(POSTOJANJE_POCETAK, True)
                elif string == '##postojanje':
                        return Token(POSTOJANJE_KRAJ, True)
                elif string == '#dodela':
                        return Token(DODELA_POCETAK, True)
                elif string == '##dodela':
                        return Token(DODELA_KRAJ, True)
                elif string == '#polje':
                        return Token(POLJE_POCETAK, True)
                elif string == '##polje':
                        return Token(POLJE_KRAJ, True)
                elif string == '#naredba':
                        return Token(NAREDBA_POCETAK, True)
                elif string == '##naredba':
                        return Token(NAREDBA_KRAJ, True)
                elif string == '#celina':
                        return Token(CELINA_POCETAK, True)
                elif string == '##celina':
                        return Token(CELINA_KRAJ, True)
                elif string == '#rutina':
                        return Token(RUTINA_POCETAK, True)
                elif string == '#rutina':
                        return Token(RUTINA_KRAJ, True)
                elif string == '#~rutina':
                        return Token(RUTINA_POZIV_POCETAK, True)
                elif string == '##~rutina':
                        return Token(RUTINA_POZIV_KRAJ, True)
                elif string == '#~ugradjena_rutina':
                        return Token(UGRADJENA_RUTINA_POZIV_POCETAK, True)
                elif string == '##~ugradjena_rutina':
                        return Token(UGRADJENA_RUTINA_POZIV_KRAJ, True)
                elif string == '#vrati':
                        return Token(VRATI_POCETAK, True)
                elif string == '##vrati':
                        return Token(VRATI_KRAJ, True)
                elif string == 'uslov':
                        return Token(NAREDBA_USLOV, True)
                elif string == 'ponavljanje':
                        return Token(NAREDA_PONAVLJANJE, True)
                elif string == 'pitanje':
                        return Token(CELINA_DA, True)
                elif string == 'da':
                        return Token(CELINA_NE, True)
                elif string == 'ne':
                        return Token(CELINA_PONOVI, True)
                elif string == 'ponovi':
                        return Token(CELINA_POLJA, True)
                elif string == 'polja':
                        return Token(CELINA_POLJA, True)
                elif string == 'sadrzaj_rutine':
                        return Token(CELINA_SADRZAJ_RUTINE, True)
                elif string == '~ceo_broj' or string == '~struna':
                        return Token(TIP_PODATKA, string)
                return Token(NAZIV, string)

        def advance(self):
                self.pos += 1
                if self.pos == len(self.text):
                        self.error("");
                self.current_char = self.text[self.pos];

        def get_next_token(self):
                self.skip_whitespace()
                if self.pos >= len(self.text):
                        return Token(EOF, None)
                current_char = self.text[self.pos]
                token = {}
                if current_char.isdigit():
                        token =  Token(CEO_BROJ, self.parse_number())
                elif self.text[self.pos].isalpha() or self.text[self.pos] == '#' or self.text[self.pos] == '~':
                        token = self.parse_keyword()
                elif current_char == '"':
                        token =  Token(STRUNA, self.parse_string())
                elif current_char == '+':
                        token =  Token(PLUS, '+')
                elif current_char == '-':
                        token = Token(MINUS, '-')
                elif current_char == '*':
                        token = Token(MNOZENJE, '*')
                elif current_char == '/':
                        token = Token(DELJENJE, '/')
                elif current_char == '%':
                        token = Token(OSTATAK, '/')
                elif current_char == '(':
                        token = Token(OTVORENA_ZAGRADA, '(')
                elif current_char == ')':
                        token = Token(ZATVORENA_ZAGRADA, ')')
                elif current_char == '<':
                        token = Token(MANJE, '<')
                elif current_char == '>':
                        token = Token(VECE, '>')
                elif current_char == '<=':
                        token = Token(MANJE_JEDNAKO, '<')
                elif current_char == '>=':
                        token = Token(VECE_JEDNAKO, '>')
                elif current_char == '=':
                        token = Token(JEDNAKO, '=')
                elif current_char == ':':
                    token = Token(COLON, ':')
                elif current_char == ',':
                    token = Token(COMMA, ',')
                elif current_char == '!':
                        self.advance()
                elif current_char == '(':
                        token = Token(OTVORENA_ZAGRADA, '(')
                elif current_char == ')':
                        token = Token(ZATVORENA_ZAGRADA, ')')
                elif current_char == '<':
                        token = Token(MANJE, '<')
                elif current_char == '>':
                        token = Token(VECE, '>')
                elif current_char == '<=':
                        token = Token(MANJE_JEDNAKO, '<')
                elif current_char == '>=':
                        token = Token(VECE_JEDNAKO, '>')
                elif current_char == '=':
                        token = Token(JEDNAKO, '=')
                elif current_char == ':':
                    token = Token(COLON, ':')
                elif current_char == ',':
                    token = Token(COMMA, ',')
                elif current_char == '!':
                        self.advance()
                        if self.current_char == '=':
                                token = Token(NIJE_JEDNAKO, '!=')
                        else:
                                token = Token(LOGICKO_NE, '!')
                                self.pos -= 1
                elif current_char == '&':
                        self.advance()
                        if self.current_char == '&':
                                token = Token(LOGICKO_I, '&&')
                elif current_char == '|':
                        self.advance()
                        if self.current_char == '|':
                                token = Token(LOGICKO_ILI, '||')
                        else:
                                token = Token(PIPE, '|')
                                self.pos -= 1
                else:
                        print("CHAR: " + current_char)
                        self.error("")
                self.pos += 1
                return token

        def error(self, current_char):
                raise Exception("Unexpected character {}".format(current_char))
