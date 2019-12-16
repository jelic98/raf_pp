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
                string = ''
                self.pos += 1
                while(self.pos < len(self.text) and self.text[self.pos] != '"'):
                        string += self.text[self.pos]
                        self.pos += 1
                return string

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
                        return Token(PROGRAM_POCETAK, string)
                elif string == '##program':
                        return Token(PROGRAM_KRAJ, string)
                elif string == '#postojanje':
                        return Token(POSTOJANJE_POCETAK, string)
                elif string == '##postojanje':
                        return Token(POSTOJANJE_KRAJ, string)
                elif string == '#dodela':
                        return Token(DODELA_POCETAK, string)
                elif string == '##dodela':
                        return Token(DODELA_KRAJ, string)
                elif string == '#polje':
                        return Token(POLJE_POCETAK, string)
                elif string == '##polje':
                        return Token(POLJE_KRAJ, string)
                elif string == '#naredba':
                        return Token(NAREDBA_POCETAK, string)
                elif string == '##naredba':
                        return Token(NAREDBA_KRAJ, string)
                elif string == '#celina':
                        return Token(CELINA_POCETAK, string)
                elif string == '##celina':
                        return Token(CELINA_KRAJ, string)
                elif string == '#rutina':
                        return Token(RUTINA_POCETAK, string)
                elif string == '##rutina':
                        return Token(RUTINA_KRAJ, string)
                elif string == '#~rutina':
                        return Token(RUTINA_POZIV_POCETAK, string)
                elif string == '##~rutina':
                        return Token(RUTINA_POZIV_KRAJ, string)
                elif string == '#~ugradjena_rutina':
                        return Token(UGRADJENA_RUTINA_POZIV_POCETAK, string)
                elif string == '##~ugradjena_rutina':
                        return Token(UGRADJENA_RUTINA_POZIV_KRAJ, string)
                elif string == '#vrati':
                        return Token(VRATI_POCETAK, string)
                elif string == '##vrati':
                        return Token(VRATI_KRAJ, string)
                elif string == '#prekini_ponavljanje':
                        return Token(PREKINI_PONAVLJANJE, string)
                elif string == 'uslov':
                        return Token(NAREDBA_USLOV, string)
                elif string == 'ponavljanje':
                        return Token(NAREDBA_PONAVLJANJE, string)
                elif string == 'pitanje':
                        return Token(CELINA_PITANJE, string)
                elif string == 'da':
                        return Token(CELINA_DA, string)
                elif string == 'ne':
                        return Token(CELINA_NE, string)
                elif string == 'ponovi':
                        return Token(CELINA_PONOVI, string)
                elif string == 'polja':
                        return Token(CELINA_POLJA, string)
                elif string == 'sadrzaj_rutine':
                        return Token(CELINA_SADRZAJ_RUTINE, string)
                elif string == '~ceo_broj' or string == '~struna' or string == '~jeste_nije':
                        return Token(TIP_PODATKA, string)
                elif string == 'jeste' or string == 'nije':
                        return Token(JESTE_NIJE, string)
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
                token = None
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
                        token = Token(OSTATAK, '%')
                elif current_char == '(':
                        token = Token(ZAGRADA_OTVORENA, '(')
                elif current_char == ')':
                        token = Token(ZAGRADA_ZATVORENA, ')')
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
                        self.error(current_char)
                self.pos += 1
                return token

        def error(self, current_char):
                raise Exception("Unexpected character {}".format(current_char))
