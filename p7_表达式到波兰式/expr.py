#!/usr/bin/env python
# encoding=utf-8
# arithmetics expression parser 
# and transform to poslish/reverse polish expressions
# caoyijun2050@gmail.com
# 曹逸君 1352872
#input 3+5*(7-8/2)
import re
from copy import deepcopy
from debug import debug, pprint, pdb

def flatten(array):
	"""
		Returns a list o flatten elements of every inner lists (or tuples)
		****RECURSIVE****
	"""
	res = []
	for el in array:
		if isinstance(el, (list, tuple)):
			res.extend(flatten(el))
			continue
		res.append(el)
	return res

class Token(object):
	""" base Token class"""
	def __init__(self, parser, string):
		super(Token, self).__init__()
		self.value = string
		self.parser = parser
	def __repr__(self):
		return "{0}({1})".format(self.__class__.__name__, self.value)
	def __eq__(self, another):
		return self.value == another

class Blank(Token):
	def __init__(self, string):
		super(Blank, self).__init__()
		self.value = re.match('^\\s+', string)

class EndToken(Token):
	left_bind_power = 0

class Num(Token):
	left_bind_power = 10
	# def __init__(self, string):
	# 	super(Num, self).__init__(string)
		# self.value = int(self.value)
	def null_denotation(self):
		return self.value

def Operator(parser, string):
	return	{	"+": Add,
				"-": Sub,
				"*": Mul,
				"/": Div,
				"(": Left_bracket,
				")": Right_bracket,
				}[string](parser, string)

class OperatorToken(Token):
	def left_denotation(self, left_expr, expr_type="Norm"):
		right_expr = self.parser.expression(self.left_bind_power)
		if expr_type=="Norm":
			return (left_expr, self.value, right_expr)
		elif expr_type=="Polish":
			return (self.value, left_expr, right_expr)
		elif expr_type=="ReversePolish":
			return (left_expr, right_expr, self.value)
		
class Add(OperatorToken):
	left_bind_power = 20

class Sub(OperatorToken):
	left_bind_power = 20

class Mul(OperatorToken):
	left_bind_power = 30

class Div(OperatorToken):
	left_bind_power = 30

class Left_bracket(Token):
	left_bind_power = 100
	def null_denotation(self):
		right_expr = self.parser.expression()
		if not isinstance(self.parser.current_token, Right_bracket):
			raise SyntaxError("Expect: {0}".format(")") )
		self.parser.next_token()
		return right_expr
class Right_bracket(Token):
	left_bind_power = 0
	# pass
	# def left_denotation(self, left_expr, expr_type="Norm"):
	# 	right_expr = self.parser.expression(self.left_bind_power)
	# 	if expr_type=="Norm":
	# 		return (left_expr, self.value, right_expr)
	# 	elif expr_type=="Polish":
	# 		return (self.value, left_expr, right_expr)
	# 	elif expr_type=="ReversePolish":
	# 		return (left_expr, right_expr, self.value)

class Parser(object):
	# expr_type = "Norm"
	def __init__(self, raw, expr_type="Norm"):
		super(Parser, self).__init__()
		self.expr_type = expr_type
		self.tokens = self.tokenize(raw)
		self.current_token = next(self.tokens)
		self.tree = self.expression()
		if self.expr_type != "Norm":
			self.result = ' '.join(flatten(self.tree))
		else:
			self.result = str(self.tree)
		print(self.expr_type)
		print(self.result)
	def next_token(self):
		self.current_token = next(self.tokens)
	def tokenize(self, raw):
		ptn = re.compile("\s*(?:(\d+)|(.))")
		parts = re.findall(ptn, raw)
		for num, operator in parts:
			if num:
				yield Num(self, num)
			elif operator:
				yield Operator(self, operator)
		yield EndToken(self, None)
	def expression(self, right_bind_power=0):
		prev = self.current_token
		self.next_token()
		left_expr = prev.null_denotation()
		# pdb.set_trace()
		while right_bind_power < self.current_token.left_bind_power:
			prev = self.current_token
			self.next_token()
			left_expr = prev.left_denotation(left_expr, self.expr_type)
		return left_expr

@debug
def main():
	# raw = "31/54 *  27 -8  	/2"
	# Parser("(1+2)*3")
	tests = [	"1+2",
				"1+3*3",
				"(3+2)*3",
				"1*3/2-4/2",
				"1*3/(6-4)/2",]
	for test in tests:
		Parser(test)
		Parser(test, "Polish")
		Parser(test, "ReversePolish")
		print
if __name__ == '__main__':
	main()