from token import Token
from type import *

class Lexer():
    def __init__(self, text, pos = 0):    
        self.text = text
        self.pos = pos

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

    def msg_error(self, msg):
        raise Exception(msg)

    def parse_function(self):
        name = ''
        space = False

        start_pos = self.pos

        while(self.pos < len(self.text) and self.text[self.pos] != '('):
            if self.text[self.pos].isalpha():
                if space:
                    self.msg_error("Function name cannot include space")
                name += self.text[self.pos]
            space = self.text[self.pos].isspace()
            self.pos += 1
        
        if((self.pos < len(self.text) and self.text[self.pos] != '(') or self.pos >= len(self.text)):
            return None

        self.pos += 1

        params = []
        pname = ""

        self.skip_whitespace()
        
        while(self.pos < len(self.text) and self.text[self.pos].isalnum()):
            pname += self.text[self.pos]
            self.pos += 1
            self.skip_whitespace()
            if self.text[self.pos] in [',', ')']:
                params.append(pname)
                pname = ""
                self.pos += 1
                self.skip_whitespace()
         

        if self.text[self.pos - 1] != ')':
            elf.msg_error("Parameter list must end with parameter")

        fun = {}
        fun["name"] = name
        fun["params"] = params
        fun["calls"] = []

        fun_call = self.text[start_pos:self.pos]

        return (fun, fun_call)

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
            token =  Token(FUN, self.parse_function())
        else:
            self.error("")

        self.pos += 1
        return token

    def error(self, token_type):
        raise Exception("expected {} but found {}".format(token_type, ""))
