from pyvis.network import Network
import networkx as nx
import time

start = time.time()

net = Network()

nodes = ['A', 'B', 'C', 'D', 'E']
net.add_nodes(nodes)

net.enable_physics(True)

end = time.time() - start
print("Program executed in %.4f seconds" % end)

net.show('graph.html')
