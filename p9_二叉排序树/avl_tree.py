#!/usr/bin/env python
# encoding=utf-8
# AVL tree
# caoyijun2050@gmail.com
# 曹逸君 1352872
# a implementation of AVL tree
# a nice animation here https://www.cs.usfca.edu/~galles/visualization/AVLtree.html


from debug.debug import debug, pdb, pprint
from ete2 import Tree, TreeStyle

raw = [12, 34, 67, 48, 19, 44, 21, 30, 19, 7, 4, 24, 9, 88, 100, 100, 0]

class Node(object):
	""" Node in a AVL tree
		Note that i add parent attr to 
		avoid use recursive calls
	"""
	def __init__(self, key=None, parent=None, left_child=None, right_child=None):
		super(Node, self).__init__()
		self.key = key
		self.parent = parent
		self.left_child = left_child
		self.right_child = right_child
		self.update_height()
	def leftRotate(self):
		pivot = self.right_child
		# transfer pivots' left_child to root
		trans = pivot.left_child
		self.right_child = trans
		if trans:
			trans.parent = self
		# exchange child-parent
		if self.parent:   # trouble with parent
			if self.parent.left_child is self:
				self.parent.left_child = pivot
			else:
				self.parent.right_child = pivot
		pivot.parent = self.parent
		self.parent = pivot
		pivot.left_child = self
		# update height
		self.update_height()
		if pivot.right_child:
			pivot.right_child.update_height()
		return pivot
		pivot.update_height()
	def rightRotate(self):
		pivot = self.left_child
		# transfer pivots' right_child to root
		trans = pivot.right_child
		self.left_child = trans
		if trans:
			trans.parent = self
		# exchange child-parent
		if self.parent:   # trouble with parent
			if self.parent.left_child is self:
				self.parent.left_child = pivot
			else:
				self.parent.right_child = pivot
		pivot.parent = self.parent
		self.parent = pivot
		pivot.right_child = self
		# update height
		self.update_height()
		if pivot.left_child:
			pivot.left_child.update_height()
		pivot.update_height()
		return pivot
	def update_height(self):
		l_height = self.left_child.height if self.left_child else 0
		r_height = self.right_child.height if self.right_child else 0
		self.height = max(l_height, r_height) + 1
	def __repr__(self):
		return str(self.tolist())
	def tolist(self):
		tup = tuple([one for one in (self.l_tolist(), (self.key, self.height), self.r_tolist()) if one])
		if len(tup)==1:
			return tup[0]
		return tup
	def l_tolist(self):
		return None if self.key is None or self.left_child is None else self.left_child.tolist()
	def r_tolist(self):
		return None if self.key is None or self.right_child is None else self.right_child.tolist()

class DuplicateKey(Exception):
	def __init__(self, arg):
		self.arg = arg

class AVL(object):
	"""AVL tree"""
	def __init__(self):
		super(AVL, self).__init__()
		# forbid replicated keys
		self.distinct_keys = True
		self.root = Node()
	def rebalance(self, position, key):
		while position is not None:   # check till root
			position.update_height()
			position = self._rebalance(position, key)
	def _rebalance(self, position, key):
		l_height = position.left_child.height if position.left_child else 0
		r_height = position.right_child.height if position.right_child else 0
		# part 0 check for unbalance eg: (left_child.height - right_child.height) > 1
		diff = l_height - r_height
		# Left Left
		if diff > 1 and key < position.left_child.key:
			pivot = position.rightRotate()
		# Right Right
		elif diff < -1 and key > position.right_child.key:
			pivot = position.leftRotate()
		# Left Right
		elif diff > 1 and key > position.left_child.key:
			pivot = position.left_child.leftRotate()
			pivot = position.rightRotate()
		# Right Left
		elif diff < -1 and key < position.right_child.key:
			pivot = position.right_child.rightRotate()
			pivot = position.leftRotate()
		else:   # no rotate performed
			return position.parent   #next_position
		if pivot.parent is None:
			self.root = pivot
		return pivot.parent
	def insert(self, key):
		if self.root.key is None:
			self.root.key = key
		else:
			try:
				position, left = self.search(key)
			except DuplicateKey as e:
				return # ignore DuplicateKeys
			if left:
				position.left_child = Node(key=key, parent=position)
			else:
				position.right_child = Node(key=key, parent=position)
			self.rebalance(position, key)
	def find(self, key):
		try:
			position, left = self.search(key)
		except DuplicateKey as e:
			return e.arg
		return None
	def search(self, key):
		position = self.root
		while True:
			if key == position.key:
				raise DuplicateKey(position.key)
			left = key < position.key
			_tmp = position.left_child if left else position.right_child
			if _tmp is None:  # not exists
				return position, left
			position = position.left_child if left else position.right_child
	def __repr__(self):
		return self.root.__repr__()
	def show(self, i=0):
		t = Tree(str(self)+";")
		ts = TreeStyle()
		ts.show_leaf_name = True
		ts.rotation = 90
		t.render("mytree-{0}.png".format(i), w=183, units="mm", tree_style=ts)
		t.show(tree_style=ts)

@debug
def main():
	tree = AVL()
	for i, one in enumerate(raw):
		tree.insert(one)
		tree.show(i)
	print tree
	print tree.find(21)
	print tree.find(34)
	print tree.find(100)
	print tree.find(1030)
if __name__ == '__main__':
	main()