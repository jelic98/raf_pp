from token import Token
from type import *
from lexer import Lexer

# FUNCTION MAP
# _def --> fun(a, b, c)
# _def --> a + b + c
# "fun" -> [
#   "name" -> "fun"
#   "params" -> [a, b, c],
#   "expr" -> "a + b + c",
#   "stack" -> [CALL STACK]
# ]

# input_mode = 1 ; normal mode
# input_mode = 2 ; define mode signature
# input_mode = 3 ; define mode body

input_mode = 2;
funs = {}
last_fun = None

class Interpreter():
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, token_type):
        raise Exception("Expected {} but found {}".format(token_type, self.current_token.token_type))

    def msg_error(self, msg):
        raise Exception(msg)

    def eat(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)

    def factor(self):
        token = self.current_token
        
        if token.token_type == FUN:
            fun = token.value[0]
            
            if not fun["name"] in funs:
                msg_error("Function not defined")
            
            fun_defined = funs[fun["name"]]
            
            if len(fun["params"]) != len(fun_defined["params"]):
                self.msg_error("Calling function {} with {} instead of {} parameters".format(fun["name"], len(fun["params"]), len(fun_defined["params"])))
            
            pos = 0
            expr = "(" + fun_defined["expr"] + ")"
            fun = token.value[0]
            fun_call = token.value[1]
            
            for param in fun_defined["params"]:
                expr = expr.replace(param, fun["params"][pos])
                pos += 1
            
            self.lexer.pos = self.lexer.text.find(fun_call) + 1
            self.lexer.text = self.lexer.text.replace(fun_call, expr, 1)

            print("TEXT: " + self.lexer.text + " " + self.lexer.text[self.lexer.pos:])
            self.current_token = Token(LPAREN, "(")

            return self.factor()
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

    def define(self):
        global funs, last_fun
        token = self.current_token
        fun = token.value[0]

        for param in fun["params"]:
            if not param[0].isalpha():
                self.msg_error("Parameter list must start with parameter")

        funs[fun["name"]] = fun
        last_fun = fun["name"]
        return token
    
    def define_body(self, text):
        global funs, last_fun
        if last_fun is not None:
            funs[last_fun]["expr"] = text

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
         
        if input_mode == 1:
            lexer = Lexer(text)
            intepreter = Interpreter(lexer)
            result = intepreter.expr()
            print("<-- {}".format(result))
        elif input_mode == 2:
            lexer = Lexer(text)
            intepreter = Interpreter(lexer)
            intepreter.define()
            input_mode = 3
        elif input_mode == 3:
            intepreter.define_body(text)
            input_mode = 1

if __name__ == "__main__":
    main()
