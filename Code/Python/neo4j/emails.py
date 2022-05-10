from py2neo import Database, Graph
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import time

s = time.time()

# Start of connection
db = Database()
g = Graph('bolt://localhost:7687', auth=('neo4j', 'super'))

# Get all mails sent
query = """
MATCH (sender:Address)-[r]->(receiver:Address)
RETURN sender.id, receiver.id
"""
d = g.run(query).data()
data = []
for el in d:
    data.append((el['sender.id'], el['receiver.id']))

# Create network
G = nx.from_edgelist(data)
nx.draw_networkx(G)

final = time.time()-s
print('Program executed in {0:.4f} seconds'.format(final))

plt.show()

# End of connection
db.shutdown()
