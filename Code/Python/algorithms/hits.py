import numpy as np
import matplotlib.pyplot as plt

n = 5
it = 10

def hits(M, auth, hubs):
    """Performs the HITS algorithms
    Parameters
    ----------
    M : numpy array
        adjacency matrix
    auth : vector (1D numpy array)
        vector of authorities
    hubs : vector (1D numpy array)
        vector of hubs

    Returns
    -------
    2 numpy arrays
        Array of authorities and hubs
    """
    tmp_a, tmp_h = np.ones(n), np.ones(n)
    arr_a, arr_h = tmp_a, tmp_h
    for k in range(it):
        for i in range(n):
            auth[i] = np.dot(tmp_h, mat[:,i]) # iterate through each column
            hubs[i] = np.dot(tmp_a, mat[i]) # iterate through each line
        nb_a, nb_h = np.sum(auth), np.sum(hubs)
        if nb_a != 0 and nb_h != 0:
            auth = np.true_divide(auth, nb_a)
            hubs = np.true_divide(hubs, nb_h)
        tmp_a, tmp_h = auth, hubs
        arr_a = np.vstack((arr_a, tmp_a))
        arr_h = np.vstack((arr_h, tmp_h))
    i = [x for x in range(it+1)]
    for node in range(n):
        plt.plot(i, [aut[node] for aut in arr_a], label=('Page %d authority score' % node))
        plt.plot(i, [hub[node] for hub in arr_h], label=('Page %d hub score' % node))
    return auth, hubs


if __name__ == '__main__':
    # Graph construction
    a = np.random.randint(2, size=(n, n))
    inverse = 1-np.eye(n, dtype=np.int)
    mat = np.bitwise_and(a, inverse)
    mat = np.array([[0,1,1,0,0],[1,0,0,1,1],[0,1,0,0,0],[1,0,1,0,0],[1,0,1,1,0]])

    # Hubs and authorities
    auth, hubs = np.ones(n), np.ones(n)

    # HITS algorithm
    print(mat)
    hits(mat, auth, hubs)

    plt.xlabel('Itération')
    plt.ylabel('Scores')
    plt.title('Résultats de l\'algorithme HITS')
    plt.legend(loc='upper right')
    plt.plot()
    plt.show()
