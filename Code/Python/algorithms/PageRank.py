import matplotlib.pyplot as plt
import time

def pageRank(dict, d, it):
    """
    Computes PageRank algorithm using a dictionnary as data structure
    """
    # Graph parameters
    vertices = list(dict.keys())
    n = len(vertices)
    init_pr = 1/n
    for k,v in dict.items():
        v['pr'] = [init_pr]

    # PageRank algorithm
    for i in range(it):
        for k,v in simple_web.items():
            pr = 0
            # Run through all links that refer selected page
            for ws,params in simple_web.items():
                if k in params['links']:
                    pr += params['pr'][i]/len(params['links'])
            # New page rank calculation
            v['pr'].append((1-d) + d*pr)

    x = [i for i in range(it+1)]
    for k,v in dict.items():
        print('PR(%s) = %f' % (k, v['pr'][it]))
        plt.plot(x, v['pr'], label=('Website %s' % k))


# Result part
if __name__ == '__main__':
    start = time.time()
    # Graph construction
    simple_web = {
        'a': {'links': ['c', 'j'], 'pr': [0]},
        'b': {'links': ['c', 'i'], 'pr': [0]},
        'c': {'links': ['a', 'b', 'd', 'e', 'f', 'g', 'h', 'i', 'j'], 'pr': [0]},
        'd': {'links': ['b', 'c', 'i'], 'pr': [0]},
        'e': {'links': ['c', 'f', 'h', 'i', 'j'], 'pr': [0]},
        'f': {'links': ['b', 'c', 'g', 'j'], 'pr': [0]},
        'g': {'links': ['c', 'd', 'h', 'i'], 'pr': [0]},
        'h': {'links': ['a', 'c'], 'pr': [0]},
        'i': {'links': ['b', 'c', 'd', 'g', 'j'], 'pr': [0]},
        'j': {'links': ['c', 'e'], 'pr': [0]},
    }

    pageRank(simple_web, .85, 20)
    print('Finished in %f seconds' % float(time.time() - start))

    plt.xlabel('Nombre d\'itérations')
    plt.ylabel('Valeur du PageRank')
    plt.title('Evolution des valeurs du PageRank de chaque page')
    plt.legend(loc='upper right')
    plt.plot()
    plt.show()
