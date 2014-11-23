#!/usr/bin/env python
# encoding=utf-8
# prim algorithm to find MST
# caoyijun2050@gmail.com
# 曹逸君 1352872

# from debug.debug import debug, pdb, pprint

V = ['a', 'b', 'c', 'd']
E = [('a', 'b', 8), ('b', 'c', 7), ('c', 'd', 5), ('d', 'a', 11), ('a', 'c', 18), ('b', 'd', 12)]
neighbours = {v: [] for v in V}
for u,w,d in E:
	neighbours[u] .append((w, d))
	neighbours[w] .append((u, d))

# @debug
def prim(V, E):
	V_new = [V[0]]  # start vertex random would do
	E_new = []
	while len(V_new) < len(V):
		tmp  = None
		for v in V_new:
			for nei in neighbours[v]:
				if nei[0] in V_new:
					continue
				if tmp is None:
					tmp = (v, nei[0], nei[1])
				elif tmp[2] > nei[1]:
					tmp = (v, nei[0], nei[1])
		V_new.append(tmp[1])
		E_new.append(tmp)
	print V_new
	print E_new

if __name__ == '__main__':
	prim(V, E)