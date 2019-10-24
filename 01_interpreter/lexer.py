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

    # parse funciton (only in input_mode = 2)
    def parse_function(self):
        name = ''
        space = False

        start_pos = self.pos

        # get function name
        while(self.pos < len(self.text) and self.text[self.pos] != '('):
            if self.text[self.pos].isalpha():
                name += self.text[self.pos]

            # skip space in function name
            space = self.text[self.pos].isspace()
            self.pos += 1
        
        # check if function definition (input_mode = 2) or its usage (input_mode = 1,3) is correct
        if((self.pos < len(self.text) and self.text[self.pos] != '(') or self.pos >= len(self.text)):
            return None

        self.pos += 1

        params = []
        pname = ""
        
        # skip whitespace between parenthesis and first parameter
        self.skip_whitespace()

        # get function parameters
        while(self.pos < len(self.text) and self.text[self.pos].isalnum()): 
            # create temporary string that will hold parameter names
            pname += self.text[self.pos]
            self.pos += 1
            
            # skip whitespace between parameters and commas
            self.skip_whitespace()
           
            # check if there is more parameters to parse
            if(self.pos < len(self.text) and self.text[self.pos] == ','):
                # add parameter to function parameter list 
                params.append(pname)
            
                # reset current parameter name to parse next one
                pname = ""
                self.pos += 1

                # skip whitespace between parameters and commas
                self.skip_whitespace()
        
        params.append(pname)
        
        if self.text[self.pos] != ')':
            print("Function signature not valid")
            return None

        self.pos += 1

        # create function (input_mode = 1, 2, 3)
        fun = {}
        fun["name"] = name
        fun["params"] = params
        fun["calls"] = []

        fun_call = self.text[start_pos:self.pos]

        # this is tupple because we need reference to defined function
        # as well as it concrete usage in input_mode = 1
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
        # since we are not using variables in input_mode = 1
        # checking if current char is letter is okay
        # for checking if next token is function
        elif current_char.isalpha():
            token =  Token(FUN, self.parse_function())
        else:
            self.error("")

        self.pos += 1
        return token

    def error(self, token_type):
        raise Exception("expected {} but found {}".format(token_type, ""))
