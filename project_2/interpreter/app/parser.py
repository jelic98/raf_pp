from app.type import *
from app.nodes import *
from functools import wraps
import pickle

class Parser():
	def __init__(self, lexer):
		self.lexer = lexer
		self.current_token = self.lexer.get_next_token()

	def restorable(fn):
		@wraps(fn)
		def wrapper(self, *args, **kwargs):
			state = pickle.dumps(self.__dict__)
			result = fn(self, *args, **kwargs)
			self.__dict__ = pickle.loads(state)
			return result
		return wrapper

	@restorable
	def check_function(self):
		self.eat(TYPE)
		self.eat(ID)
		return self.current_token.token_type == LPAREN

	def error(self, token_type):
		raise Exception("expected {} but found {}".format(token_type, self.current_token.token_type))

	def type_error(self, expected, found):
		raise Exception("Expected: {}, but found: {}".format(expected, found))

	def eat(self, token_type):
		if self.current_token.token_type == token_type:
			self.current_token = self.lexer.get_next_token()
		else:
			self.error(token_type)

	def program(self):
		child_nodes = []
		while self.current_token.token_type != EOF:
			if self.current_token.token_type == HASH:
				child_nodes.append(self.include_library())
			elif self.current_token.token_type == TYPE:
				if self.check_function():
					child_nodes.append(self.function_declaration())
				else:
					child_nodes.extend(self.var_declaration_list())
			else:
				self.error('HASH or TYPE')
		return Program(child_nodes)

	def function_declaration(self):
		f_type = Type_node(self.current_token.value)
		self.eat(TYPE)
		f_name = self.current_token.value
		self.eat(ID)
		self.eat(LPAREN)
		self.eat(RPAREN)
		f_body = self.body()
		return Fun_Decl(f_type, f_name, None, f_body)

	def body(self, brackets = True):
		if brackets:
			self.eat(LBRACKET)
		stmts = []
		if brackets:
			while self.current_token.token_type != RBRACKET:
				stmt = self.statement()
				if type(stmt).__name__ == 'list':
					stmts.extend(stmt)
				else:
					stmts.append(stmt)
		else:
			stmt = self.statement()
			if type(stmt).__name__ == 'list':
				stmts.extend(stmt)
			else:
				stmts.append(stmt)
		if brackets:
			self.eat(RBRACKET)
		return Body(stmts)

	def statement(self):
		if self.current_token.token_type == IF:
			return self.if_stmt()
		elif self.current_token.token_type == TYPE:
			return self.var_declaration_list()
		else:
			self.error('some statement')

	def if_stmt(self):
		self.eat(IF)
		self.eat(LPAREN)
		condition = self.logic()
		self.eat(RPAREN)
		body = None
		else_body = None
		if self.current_token.token_type == LBRACKET:
			body = self.body()
		else:
			body = self.body(False)
		if self.current_token.token_type == ELSE:
			self.eat(ELSE)
			if self.current_token.token_type == LBRACKET:
				else_body = self.body()
			else:
				else_body = self.body(False)
		return If_Stmt(condition, body, else_body)

	def var_declaration_list(self):
		declarations = []
		type_node = Type_node(self.current_token.value)
		self.eat(TYPE)
		var_node = Variable(self.current_token.value)
		self.eat(ID)
		declarations.extend(self.var_declaration(type_node, var_node))
		while self.current_token.token_type == COMMA:
			self.eat(COMMA)
			var_node = Variable(self.current_token.value)
			self.eat(ID)
			declarations.extend(self.var_declaration(type_node, var_node))
		self.eat(SEMICOLON)
		return declarations

	def var_declaration(self, type_node, var_node):
		declarations = []
		declarations.append(Var_Decl(type_node, var_node))
		if self.current_token.token_type == ASSIGN:
			self.eat(ASSIGN)
			declarations.append(Assign(var_node, self.logic()))
		return declarations

	def include_library(self):
		pass

	def factor(self):
		token = self.current_token
		if token.token_type == INTEGER:
			self.eat(INTEGER)
			return Num(token.value)
		elif token.token_type == BOOLEAN:
			self.eat(BOOLEAN)
			return Num(token.value)
		elif token.token_type in [NOT, MINUS]:
			op_token = self.current_token
			if op_token.token_type == MINUS:
				self.eat(MINUS)
			elif op_token.token_type == NOT:
				self.eat(NOT)
			result = None
			if self.current_token.token_type == LPAREN:
				self.eat(LPAREN)
				result = self.logic()
				self.eat(RPAREN)
			else:
				result = self.factor()
			if op_token.token_type == NOT:
				self.check_logic(result)
			return UnOp(op_token.value, result)
		elif token.token_type == LPAREN:
			self.eat(LPAREN)
			result = self.logic()
			self.eat(RPAREN)
			return result

	def term(self):
		left_node = self.factor()
		while self.current_token.token_type in [MUL, DIV]:
			if self.current_token.token_type == MUL:
				self.eat(MUL)
				right_node = self.factor()
				left_node = BinOp(left_node, '*', right_node)
			elif self.current_token.token_type == DIV:
				self.eat(DIV)
				right_node = self.factor()
				left_node = BinOp(left_node, '/', right_node)
		return left_node

	def expr(self):
		left_node = self.term()
		while self.current_token.token_type in [PLUS, MINUS]:
			if self.current_token.token_type == PLUS:
				self.eat(PLUS)
				right_node = self.term()
				left_node = BinOp(left_node, '+', right_node)
			elif self.current_token.token_type == MINUS:
				self.eat(MINUS)
				right_node = self.term()
				left_node = BinOp(left_node, '-', right_node)
		return left_node

	def compare(self):
		left_node = self.expr()
		if self.current_token.token_type == GREATER:
			self.eat(GREATER)
			right_node = self.expr()
			left_node = BinOp(left_node, '>', right_node)
		elif self.current_token.token_type == LESS:
			self.eat(LESS)
			right_node = self.expr()
			left_node = BinOp(left_node, '<', right_node)
		elif self.current_token.token_type == EQUALS:
			self.eat(EQUALS)
			right_node = self.expr()
			left_node = BinOp(left_node, '==', right_node)
		elif self.current_token.token_type == NOT_EQUALS:
			self.eat(NOT_EQUALS)
			right_node = self.expr()
			left_node = BinOp(left_node, '!=', right_node)
		return left_node

	def check_logic(self, node):
		if str(type(node).__name__) == 'Num':
			if type(node.num).__name__ != 'bool':
				self.type_error('bool type ', type(node.num).__name__)
		elif str(type(node).__name__) == 'BinOp':
			if node.op not in ['<', '>', '>=', '<=', '==', '!=']:
				self.type_error('logical operator ', node.op)
		elif str(type(node).__name__) == 'UnOp':
			if node.op not in ['not']:
				self.type_error('not', node.op)
		else:
			self.type_error('Node of type BinOp or Num', str(type(node).__name__))

	def logic(self):
		left_node = self.compare()
		if self.current_token.token_type == AND:
			self.eat(AND)
			self.check_logic(left_node)
			right_node = self.compare()
			self.check_logic(right_node)
			left_node = BinOp(left_node, 'and', right_node)
		elif self.current_token.token_type == OR:
			self.eat(OR)
			self.check_logic(left_node)
			right_node = self.compare()
			self.check_logic(right_node)
			left_node = BinOp(left_node, 'or', right_node)
		return left_node
