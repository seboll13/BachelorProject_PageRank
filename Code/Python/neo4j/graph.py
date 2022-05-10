import matplotlib.pyplot as plt
import networkx as nx
import dynetx as dn
import time

# Start of program
start = time.time()

# Graph creation
G = nx.DiGraph()
nodes = ['A', 'B', 'C', 'D', 'E']
G.add_nodes_from(nodes)
edges = [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'D'), ('B', 'E'), ('C', 'B'), ('C', 'E'), ('D', 'A'), ('D', 'C'),
         ('E', 'A'), ('E', 'C'), ('E', 'D')]
G.add_edges_from(edges)

# Graph manipulation
nx.draw(G, with_labels=1)

# End of program
print("Program executed in %.4f seconds" % (time.time()-start))

plt.show()
