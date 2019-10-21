from token import Token
from type import *
from lexer import Lexer

# FUNCTION MAP
# def: f(a, b, c)
# def: a + b + c
# f -> [
#   "params" -> [a, b, c],
#   "expr" -> "a + b + c",
#   "stack" -> [CALL STACK]
# ]

# input_mode = 1 ; normal mode
# input_mode = 2 ; define mode signature
# input_mode = 3 ; define mode body

input_mode = 2;
funs = []

class Interpreter():
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, token_type):
        raise Exception("Expected {} but found {}".format(token_type, self.current_token.token_type))

    def eat(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)

    def factor(self):
        token = self.current_token
        if token.token_type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.token_type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        elif token.token_type == MINUS:
            self.eat(MINUS)
            value = self.current_token.value
            self.eat(INTEGER)
            return (-1 * value)

    def term(self):
        left = self.factor()
        
        while self.current_token.token_type in [MUL, DIV]:
            if self.current_token.token_type == MUL:
                self.eat(MUL)
                right = self.factor()
                left = left * right
            elif self.current_token.token_type == DIV:
                self.eat(DIV)
                right = self.factor()
                left = left / right

        return left

    def expr(self):
        left = self.term()

        while self.current_token.token_type in [PLUS, MINUS]:
            if self.current_token.token_type == PLUS:
                self.eat(PLUS)
                right = self.term()
                left = left + right
            elif self.current_token.token_type == MINUS:
                self.eat(MINUS)
                right = self.term()
                left = left - right

        return left        

    def exprdef(self):
        token = self.current_token
        funs.append(token.value)
        print(funs)
        return token

def main():
    global input_mode;

    while True:
        if input_mode == 2 or input_mode == 3:
            text = input("_def --> ")
        else:
            text = input("--> ")

        if not text:
            continue
        
        if text == 'def':
            input_mode = 2
            continue

        if text == 'exit':
            break

        lexer = Lexer(text)
        intepreter = Interpreter(lexer)
        
        if input_mode == 1:
            result = intepreter.expr()
            print("<-- {}".format(result))
        elif input_mode == 2:
            result = intepreter.exprdef()
            input_mode = 3
        elif input_mode == 3:
            input_mode = 1

if __name__ == "__main__":
    main()
