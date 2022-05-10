from py2neo import Database, Graph
import matplotlib.pyplot as plt

# Start of connection
db = Database()
g = Graph('bolt://localhost:7687', auth=('neo4j', 'super'))

nb_ite = 20

def clean_node_properties():
    """Remove all non useful node properties"""
    for it in range(1, nb_ite+1):
        query = g.run(
            "MATCH (n:Website)"
            "REMOVE n.pr" + str(it)
        )
    return True

def add_node_properties():
    """Calculate iterative pagerank for all biggest 10 nodes"""
    for it in range(1, nb_ite+1):
        # Run PageRank algorithm from Neo4j
        s = str(it)
        p = g.run(
            "CALL algo.pageRank('Website', 'LINK', {write:true, writeProperty:'pr" + s + "', iterations:" + s + "})"
        ).data()

        r = g.run(
            "MATCH (n) "
            "RETURN n "
            "ORDER BY n.pr" + s + " DESC LIMIT 10"
        ).data()
        #print("{}: {}\n".format(it, r))
    return True

#clean_node_properties()
#add_node_properties()

query = g.run(
    "MATCH (n) "
    "RETURN n "
    "ORDER BY n.pagerank DESC LIMIT 10"
).data()

# Create dictionnary of all pageranks associated to nodes
id = {}
for i in range(10):
    id[query[i]['n']['id']] = [query[i]['n']['pr'+str(j)] for j in range(1, nb_ite+1)]
#print(id)

for k,v in id.items():
    plt.plot([_ for _ in range(1, 21)], v)

plt.xlabel('Nombre d\'itérations')
plt.ylabel('Valeur du PageRank')
plt.title('Evolution des valeurs du PageRank de chacun des 10 meilleurs noeuds')
plt.legend(labels=id.keys(), loc='lower right')
plt.show()
