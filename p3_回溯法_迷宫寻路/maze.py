#!/usr/bin/env python
# encoding=utf-8
# maze solving[back tracking]

from debug import debug, pprint, pdb

class Maze(object):
	"""7x7 Maze"""
	maze = [ 	list("#######"),
				list("#0#000#"),
				list("#0#0###"),
				list("#000#0#"),
				list("#0#000#"),
				list("#0#0#0#"),
				list("#######"),
				]
	solved = False
class Point(object):
	"""a Point in the maze"""
	def __init__(self, *arg):
		super(Point, self).__init__()
		if len(arg) == 2:
			self.row = arg[0]
			self.col = arg[1]
		else:
			self.row = arg[0].row
			self.col = arg[0].row
	def __eq__(self, another):
		return self.row == another.row and self.col == another.col
	def __repr__(self):
		return "Point({0}, {1})".format(self.row, self.col)
	def block(self):
		return Maze.maze[self.row][self.col]
	def mark_walked(self):
		Maze.maze[self.row][self.col] = 'x'
		pprint(Maze.maze)
		print
	def walkable(self):
		block = self.block()
		if block == '#' or block == 'x':
			return False
		else:
			return True
	def get_directions(self):
		directions = [Point(self.row, self.col-1), Point(self.row-1, self.col), Point(self.row, self.col+1), Point(self.row+1, self.col)]
		directions = [direction for direction in directions if direction.walkable()]
		return directions
	def move(self, end_point):
		if Maze.solved:
			return True
		self.mark_walked()
		if self == end_point:
			Maze.solved = True
			return True
		for direction in self.get_directions():
			direction.move(end_point)
@debug
def main():
	start_point = Point(1,1)
	end_point = Point(5,5)
	start_point.move(end_point)
	pprint(Maze.maze)

if __name__ == '__main__':
	main()