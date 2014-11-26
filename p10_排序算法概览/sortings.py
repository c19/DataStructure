#!/usr/bin/env python
# encoding=utf-8
# implementation and compare between major sorting algorithms
# caoyijun2050@gmail.com
# 曹逸君 1352872
# great visualizations sites: http://sortvis.org/ http://sorting.at/

from debug.debug import debug, pdb, pprint

import random

import pstats, StringIO
from cProfile import Profile

def random_list(size=10):
	mylist = range(size)
	random.shuffle(mylist)
	return mylist

def counter(func):
	"""
		a decoartor that provide func.count method,
		wich increase func._count_ [default increase by 1]
		used to track how many operations a function made
	"""
	def wrap(*arg, **kwarg):
		return func(*arg, **kwarg)
	wrap.__name__ = func.__name__
	wrap.__dict__['_count_'] = 0
	def inc_count(inc=1):
		wrap._count_ += inc
	wrap.__dict__['count'] = inc_count
	return wrap

def quick_sort(mylist):
	if len(mylist) <= 1:
		return mylist
	pivot = random.sample(mylist, 1)[0]  # pick random pivot
	return quick_sort([one for one in mylist if one < pivot]) + [pivot] + quick_sort([one for one in mylist if one > pivot])

def insert_sort(mylist):
	sorted_list = mylist[:1]
	for one in mylist[1:]:
		inserted = False
		for i, val in enumerate(sorted_list):  # find insertation position
			if one < val:  # insert one before val
				sorted_list.insert(i, one)
				inserted = True
				break
		if not inserted:
			sorted_list.append(one)  # insert at the end
	return sorted_list

def selection_sort(mylist):
	import operator
	sorted_list = []
	while len(mylist):
		index, samllest = min(enumerate(mylist), key=operator.itemgetter(1))
		sorted_list.append(samllest)
		del mylist[index]
	return sorted_list

def bubble_sort(mylist):
	for i in reversed(range(len(mylist)-1)):
		for j in range(i):   # j and j+1 can be safely use
			if mylist[j] > mylist[j+1]:
				mylist[j], mylist[j+1] = mylist[j+1], mylist[j]
	return mylist

def merge_sort(mylist):
	if len(mylist) == 1:
		return mylist
	if len(mylist) == 2:
		if mylist[0] > mylist[1]:  #swap
				mylist[0], mylist[1] = mylist[1], mylist[0]
		return mylist
	mid = len(mylist)/2
	part1, part2 = merge_sort(mylist[:mid]), merge_sort(mylist[mid:])
	result = []
	while True:
		if len(part1) + len(part2) == 0:
			return result
		if len(part1) == 0:
			return result + part2
		elif len(part2) == 0:
			return result + part1
		if part1[0]>part2[0]:
			result.append(part2[0])
			del part2[0]
		else:
			result.append(part1[0])
			del part1[0]

def heap_sort(mylist):
	heap = []
	def lchild(i):
		return 2*i + 1
	def rchild(i):
		return 2*i + 2
	def parent(i):
		return (i-1)/2
	def add(one):
		heap.append(one)
		i = len(heap)-1
		shift_up(i)
	def shift_up(i):
		p = parent(i)
		while p>-1:
			if heap[p] > one:  # need shift up
				heap[p], heap[i] = heap[i], heap[p]
				i, p = p, parent(p)
			else:
				break
	def shift_down(i=0):
		heaplen = len(heap)
		while True:
			l, r = lchild(i), rchild(i)
			if l >= heaplen and r >= heaplen:   # i already at leaf
				break
			elif l >= heaplen or r >= heaplen:   # i have only one child
				remain = l if  l < heaplen else r
				if heap[remain] < heap[i]:
					heap[remain], heap[i] = heap[i], heap[remain]
				break
			else:  # i have both child
				tmp = l if heap[l] < heap[r] else r
				heap[i], heap[tmp] = heap[tmp], heap[i]
				i = tmp
	def pop_min():
		head, tail = 0, len(heap) - 1
		heap[head], heap[tail] = heap[tail], heap[head]
		result = heap.pop()  # return the tail
		shift_down(0)
		return result
	for one in mylist:
		i = add(one)
	result = []
	while len(heap):
		result.append(pop_min())
	return result

def bucket_sort(mylist):
	from array import array
	"""
		a crazy implementation of bucket sort.
		create n bits for n integers
	"""
	size = max(mylist) / 8 +1
	chain = array('B', (0 for _ in range(size)))
	def mark(num):
		i = num/8
		shift = 2**(num % 8)
		chain[i] = chain[i] | shift
	for one in mylist:
		mark(one)
	result = []
	checks = [2**i for i in range(8)]
	for i, one in enumerate(chain):
		for j, check in enumerate(checks):
			if one & check:
				result.append(i*8 + j)
	return result

def radix_sort(mylist):
	"""
		radix sort implementation using LSD（Least significant digital）
		and use base 10
	"""
	def flatten(somelist):
		result = []
		for one in somelist:
			result.extend(one)
		return result
	def digit(num, i):
		#return low i th digit
		return (num % 10**(i+1)) / (10**i)
	max_len = len(str(max(mylist)))
	for i in range(max_len):
		buckets = [[] for _ in range(10)]  # ten buckets for each digit
		for one in mylist:
			buckets[digit(one, i)].append(one)
		# reassemble mylist from buckets
		mylist = flatten(buckets)
	return mylist

def shell_sort(mylist):
	"""
	http://faculty.simpson.edu/lydia.sinapova/www/cmsc250/LN250_Weiss/L12-ShellSort.htm#increments
	shell sort using Sedgewick's increments
		9 * 4^i - 9 * 2^i + 1 和 2^(i+2) * (2^(i+2) - 3) + 1
		[1, 5, 19, 41, 109, 209, 505, 929 ...
	"""
	def sedgewick_seq(length):
		def seq1():
			i=0
			while True:
				yield 9 * (4**i - 2**i) + 1
				i += 1
		def seq2():
			i=0
			while True:
				yield 2**(i+2) * (2**(i+2) - 3) + 1
				i += 1
		pool = (seq1(), seq2())
		i = 0
		sequence = [next(pool[0])]
		while True:
			i = (i+1)%2
			tmp = next(pool[i])
			if tmp > length:
				break
			sequence.append(tmp)
		return sequence
	length = len(mylist)
	increments = reversed(sedgewick_seq(length/2))
	for inc in increments:
		i = 0
		while i + inc < length:
			j = i
			while mylist[j] > mylist[j+inc]:   # insert sort in collum i
				mylist[j], mylist[j+inc] = mylist[j+inc], mylist[j]
				j -= inc
				if j < 0:
					break
			i += 1
	return mylist


def test(algo, size=10000):
	mylist = random_list(size)
	profile = Profile()
	profile.enable()
	result = profile.runcall(algo, mylist)
	profile.disable()
	stringStream = StringIO.StringIO()
	sortby = 'cumulative'
	ps = pstats.Stats(profile, stream=stringStream).sort_stats(sortby)
	ps.print_stats()
	print 
	print "\t\t\t\t{0}  sorting  {1} ints".format(algo.__name__, size)
	print stringStream.getvalue()

def main():
	for algo in [bucket_sort, radix_sort, shell_sort, quick_sort]:#, heap_sort, merge_sort, insert_sort, selection_sort, bubble_sort]:
		test(algo, 100000)

mylist = random_list()

if __name__ == '__main__':
	main()