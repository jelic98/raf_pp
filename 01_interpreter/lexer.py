from token import Token
from type import *

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

    def parse_function(self):
        name = ''

        while(self.pos < len(self.text) and self.text[self.pos] != '('):
            if self.text[self.pos].isalpha():
                name += self.text[self.pos]
            self.pos += 1
        
        self.pos += 1

        params = []
        pname = ""
        
        self.skip_whitespace()
        
        while(self.pos < len(self.text) and self.text[self.pos].isalpha()):
            pname += self.text[self.pos]
            self.pos += 1
            self.skip_whitespace()
            if self.text[self.pos] in [',', ')']:
                params.append(pname)
                pname = ""
                self.pos += 1
                self.skip_whitespace()

        fun = {}
        fun["name"] = name
        fun["params"] = params
        fun["stack"] = 0

        return Token(FUN, fun)

    def get_next_token(self):
        self.skip_whitespace()

        if self.pos >= len(self.text):
            return Token(EOF, None)

        current_char = self.text[self.pos]

        token = {}

        if current_char.isdigit():
            token =  Token(INTEGER, self.parse_number())
        elif current_char == '+':
            token =  Token(PLUS, '+')
        elif current_char == '-':
            token = Token(MINUS, '-')
        elif current_char == '/':
            token = Token(DIV, '/')
        elif current_char == '*':
            token = Token(MUL, '*')
        elif current_char == '(':
            token = Token(LPAREN, '(')
        elif current_char == ')':
            token = Token(RPAREN, ')')
        elif current_char.isalpha():
            token = self.parse_function()
        else:
            self.error("")

        self.pos += 1
        return token

    def error(self, token_type):
        raise Exception("expected {} but found {}".format(token_type, ""))
