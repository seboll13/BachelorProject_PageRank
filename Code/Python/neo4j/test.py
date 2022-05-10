from py2neo.data import Node, Relationship
import time

s = time.time()
nodes = [Node('Website', name=x) for x in ['a','b','c','d','e']]

w1 = [0,0,1,1,1,2,3,3,4,4,4]
w2 = [1,2,0,3,4,1,0,2,0,2,3]
relationships = [Relationship(nodes[i], 'LINK', nodes[j]) for i,j in zip(w1,w2)]

print('Program executed in {0:.4f} seconds'.format(time.time()-s))

print(nodes, relationships)
