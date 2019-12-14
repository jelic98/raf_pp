import os
import argparse
from  graphviz import Source
from app.type import *
from app.lexer import Lexer
from app.parser import Parser
from app.interpreter import Interpreter

def interpret(text):
        lexer = Lexer(text)
        current_token = lexer.get_next_token()
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        return interpreter.parse()

def main():
        argument_parser = argparse.ArgumentParser()
        argument_parser.add_argument('path')

        arguments = argument_parser.parse_args()
        path = arguments.path

        with open(path, 'r') as input:
                result = interpret(input.read())
        
        path_dirs = os.path.splitext(path)[0].split(os.sep)
        path_dirs.insert(-1, 'ast')
        path_ast = os.sep.join(path_dirs)

        s = Source(result, filename=path_ast, format='png')
        s.view()

if __name__ == '__main__':
        main()
