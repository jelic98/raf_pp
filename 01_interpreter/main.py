from token import Token
from type import *
from lexer import Lexer

# function map
# --> def ; input_mode = 1
# _def --> fun(a, b, c) ; input_mode = 2
# _def --> a + b + c ; input_mode = 3
# "fun" -> [
#   "name" -> "fun" ; function name
#   "params" -> ["a", "b", "c"] ; function parameters
#   "expr" -> "a + b + c" ; replacement expression
#   "calls" -> [fun1, fun2] ; child functions called from parent function
# ]

# current input mode (1, 2, 3)
input_mode = 1

# every defined function
funs = {}

# last defined function
last_fun = None

class Interpreter():
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    # print custom error message
    def msg_error(self, msg):
        raise Exception(msg)

    def error(self, token_type):
        msg_error("Expected {} but found {}".format(token_type, self.current_token.token_type))

    def eat(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)

    def factor(self):
        token = self.current_token
        
        # check if current token is function (only in input_mode = 1)
        if token.token_type == FUN:
            # token value is tupple
            # first element is function map
            # second element is concrete usage of defined function
            fun = token.value[0]
            fun_call = token.value[1]
            
            # check if function is defined
            if not fun["name"] in funs:
                msg_error("Function not defined")
            
            # get defined function
            fun_defined = funs[fun["name"]]
            
            # check parameter 
            if len(fun["params"]) != len(fun_defined["params"]):
                self.msg_error("Calling function {} with {} instead of {} parameters".format(fun["name"], len(fun["params"]), len(fun_defined["params"])))
            
            pos = 0

            # put replacement expression in parenthesis to isolate computation
            expr = "(" + fun_defined["expr"] + ")"
            
            # replace defined parameters with concrete arguments
            for param in fun_defined["params"]:
                expr = expr.replace(param, fun["params"][pos])
                pos += 1
           
            # shift cursor to adapt to replacement expression 
            self.lexer.pos = self.lexer.text.find(fun_call) + 1
            self.lexer.text = self.lexer.text.replace(fun_call, expr, 1)

            # resolve expression in parenthesis
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

    # define function signature (only in input_mode = 2)
    def define(self):
        global funs, last_fun
        
        token = self.current_token
        fun = token.value[0]

        for param in fun["params"]:
            if not param[0].isalpha():
                self.msg_error("Parameter list must start with parameter")

        funs[fun["name"]] = fun
        last_fun = fun
        
        return token
    
    # checking infinite recursion
    # by searching function name in bodies of its child functions
    def check_recursion(self, search, fname):
        # for every child function
        for call in funs[fname]["calls"]:
            # if child function has same name as function we are searching for
            if search["name"] == call["name"]:
                # stop execution and print error
                self.msg_error("Infinite recursion detected")
            # else check recursively for grand children
            self.check_recursion(search, call["name"])

    # define function body (only in input_mode = 3)
    def define_body(self, text):
        global funs, last_fun

        # check if function signature is defined
        if last_fun is not None:
            # get replacement expression
            last_fun["expr"] = text
            pos = 0
        
            # check if current function is calling another function
            # that is not defined
            # otherwise add child function to "calls" list of current function
            # if function does not call another function this
            # while loop will just increment pos to the end of text
            while pos < len(text):
                # if current character is letter (beginning of function name)
                if text[pos].isalpha():
                    # create new lexer for parsing child function
                    new_lexer = Lexer(text, pos)
                    
                    # get child function token
                    call_tok = new_lexer.get_next_token()

                    # if token has value (function is correctly parser)
                    if call_tok.value is not None:
                        call = call_tok.value[0]
                        
                        # check if token is actually function
                        if call_tok.token_type == FUN:

                            # check if child function is defined
                            if call["name"] not in funs:
                                self.msg_error("Function {} not defined".format(call["name"]))

                        # append child function to children list of last defined function
                        last_fun["calls"].append(call)
                    pos = new_lexer.pos
                else:
                    pos += 1
            
            # check if defined function has infinite recursion
            self.check_recursion(last_fun, last_fun["name"])

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
        
        # input mode switching logic 1 -> 2 -> 3 -> 1
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
