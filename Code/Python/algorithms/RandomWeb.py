import csv, itertools, os, random as r, string, time
import matplotlib.pyplot as plt
from shutil import copyfile

start = time.time()

# Random graph construction
size = 26
keys = [x for x in range(size)]
values = []
for i in range(size):
    shuffle = r.sample(keys, len(keys))
    values.append({
        'links': [shuffle[k] for k in range(r.randint(1,5)) if shuffle[k] != i],
        'pr': [0]
    })
simple_web = dict(zip(keys, values))

# Simple web visualization
for k,v in simple_web.items():
    print('%s => %s' % (k, v['links']))

# Graph files creation
names = [''.join(letter) for letter in itertools.product(string.ascii_uppercase, repeat=2)]
with open('websites.csv', 'w') as w:
    with open('links.csv', 'w') as l:
        w.write('id,name\n')
        l.write('idout,idin\n')
        for i, (k,v) in enumerate(simple_web.items()):
            w.write('%s,%s\n' % (k, names[i]))
            for el in v['links']:
                l.write('%s,%s\n' % (k, el))
# OS handling
copyfile('websites.csv', '../JS/neo4j-community-3.5.5/import/websites.csv')
copyfile('links.csv', '../JS/neo4j-community-3.5.5/import/links.csv')
os.remove('websites.csv')
os.remove('links.csv')

# Parameters
n = len(keys)
init_pr = 1/n
for k,v in simple_web.items():
    v['pr'] = [init_pr]
d = 0.85 # damping factor

# PageRank algorithm
NB_ITERATIONS = 50
for i in range(NB_ITERATIONS):
    for k,v in simple_web.items():
        pr = 0
        # Run through all links that refer selected page
        for ws,params in simple_web.items():
            if k in params['links']:
                pr += params['pr'][i]/len(params['links'])
        # New page rank calculation
        v['pr'].append((1-d) + d*pr)

# Result part
x = [i for i in range(NB_ITERATIONS+1)]
for k,v in simple_web.items():
    plt.plot(x, v['pr'], label=('Website %s' % k))

plt.xlabel('Nombre d\'itérations')
plt.ylabel('Valeur du PageRank')
plt.title('Evolution des valeurs du PageRank de chaque page')
plt.legend(loc='upper right')

print('Finished in %f seconds' % float(time.time() - start))

plt.plot()
plt.show()
