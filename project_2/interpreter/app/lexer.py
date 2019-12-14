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
		while(self.pos <len(self.text) and self.text[self.pos].isdigit()):
			number += self.text[self.pos]
			self.pos += 1
		self.pos -= 1
		return int(number)

	def parse_string(self):
		string = ''
                while(self.pos <len(self.text) and (self.text[self.pos].isalpha() or self.text[self.pos].isdigit())):
			string += self.text[self.pos]
			self.pos += 1
                self.pos -= 1

		if string == 'true':
			return Token(BOOLEAN, True)
		elif string == 'false':
			return Token(BOOLEAN, False)
		elif string == 'if':
			return Token(IF, 'if')
		elif string == 'if':
			return Token(IF, 'if')
		elif string == 'else':
			return Token(ELSE, 'else')
		elif string == 'int' or string == 'float' or string == 'double' or string == 'char':
			return Token(TYPE, string)

		return Token(ID, string)

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
			token =  Token(INTEGER, self.parse_number())
		elif current_char.isalpha():
			token = self.parse_string()
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
		elif current_char == '<':
			token = Token(LESS, '<')
		elif current_char == '>':
			token = Token(GREATER, '>')
		elif current_char == '=':
			self.advance()
			if self.current_char == '=':
				token = Token(EQUALS, '==')
			else:
				token = Token(ASSIGN, '=')
				self.pos -= 1
			token = Token(ASSIGN, '=')
		elif current_char == '!':
			self.advance()
			if self.current_char == '=':
				token = Token(NOT_EQUALS, '!=')
			else:
				token = Token(NOT, 'not')
				self.pos -= 1
		elif current_char == '&':
			self.advance()
			if self.current_char == '&':
				token = Token(AND, '&&')
		elif current_char == '|':
			self.advance()
			if self.current_char == '|':
				token = Token(OR, '||')
		elif current_char == ';':
			token = Token(SEMICOLON, ';')
		elif current_char == '{':
			token = Token(LBRACKET, '{')
		elif current_char == '}':
			token = Token(RBRACKET, '}')
		elif current_char == '#':
			token = Token(HASH, '#')
		elif current_char == ',':
			token = Token(COMMA, ',')
		else:
			self.error("")

		self.pos += 1
		return token

	def error(self, current_char):
		raise Exception("unexpected character {}".format(current_char))
