#!/usr/bin/env python
# encoding=utf-8
# maze solving[back tracking]
# caoyijun2050@gmail.com
# 曹逸君 1352872

from copy import deepcopy
from debug import debug, pprint, pdb
from itertools import chain

occupied = '#'
blank = 'O'

class DeadEnd(Exception):
	pass

class Board(object):
	"""chess board"""
	def __init__(self, N):
		super(Board, self).__init__()
		self.N = N
		self.board = [[blank for _ in range(N)] for _ in range(N)]
	def place(self, row, col):
		self.board[row][col] = occupied
	def get_available(self, row):
		def col_clear(col):
			for j in range(self.N):
				if self.board[j][col] == occupied:
					return False
			return True
		def x_clear(i, j):
			def x(i, j, delta_i, delta_j):
				while i in range(self.N) and j in range(self.N):
					yield i , j
					i += delta_j
					j += delta_i
			for i, j in chain(x(i, j, 1, 1), x(i, j, 1, -1), x(i, j, -1, -1), x(i, j, -1, 1)):
				if self.board[i][j] == occupied:
					return False
			return True
		for col in range(self.N):
			if col_clear(col) and x_clear(row, col):
				yield col
	def solve(self, row):
		if row >= self.N:  # solution found
			print("#{0} Queen solution found".format(self.N))
			pprint(self.board)
			return True
		for col in self.get_available(row):
			new_board = deepcopy(self)
			new_board.place(row, col)
			# pprint(self.board)
			new_board.solve(row+1)

@debug
def main():
	n = input('输入N\n')
	board = Board(n)
	board.solve(0)

if __name__ == '__main__':
	main()