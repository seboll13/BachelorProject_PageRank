import time
import numpy as np
import logging as log
import matplotlib.pyplot as plt

def CheiRank(P, d, it):
    """Computes inverse PageRank algorithm using matrices as data structure
    Parameters
    ----------
    P : numpy array
        adjacency matrix
    d : float
        damping factor
    it : int
        number of iterations

    Returns
    -------
    numpy array
        rank vector
    """

    m, n = len(P), len(P[0])
    PR = 1/n
    # Initial PageRank vector
    PR_pj = np.array([PR for _ in range(m)]).reshape(m, 1)
    # Other variables
    PR_pi, L_pj = np.zeros(m), np.zeros(m)
    # Count number of out links for each page
    for i,r in enumerate(P):
        L_pj[i] = np.count_nonzero(r)
        log.info(i, r)
    for n in range(it):
        for i in range(m):
            sum = 0
            # Run through all IN links
            for j in range(m):
                if P[j][i] == 1:
                    sum += PR_pj[j]/L_pj[j]
            # Rank calculation
            PR_pi[i] = (1-d)+d*sum
        PR_pj = PR_pi
        PR_pi = np.zeros(m)
    return PR_pj

def stats(array, i, v, s):
    v[i] = np.var(array)
    s[i] = np.std(array)

# Result part
if __name__ == '__main__':
    start = time.time()

    # Graph construction
    n, it = 20, 10

    p_var, p_std = np.zeros(it), np.zeros(it)
    c_var, c_std = np.zeros(it), np.zeros(it)

    for i in range(it):
        a = np.random.randint(2, size=(n, n))
        inverse = 1-np.eye(n, dtype=np.int)

        p_mat = np.bitwise_and(a, inverse)
        print('PR[{}]:\n{}'.format(i, p_mat))
        pr = CheiRank(p_mat, .85, 100)
        print(pr)
        stats(pr, i, p_var, p_std)

        c_mat = np.bitwise_and(np.transpose(a), inverse)
        print('CR[{}]:\n{}'.format(i, c_mat))
        cr = CheiRank(c_mat, .85, 100)
        print(cr)
        stats(cr, i, c_var, c_std)

    print('Finished in %f seconds' % float(time.time() - start))

    i = [x for x in range(it)]
    plt.plot(i, p_var, label=('PR Variance'))
    plt.plot(i, c_var, label=('CR Variance'))
    plt.plot(i, p_std, label=('PR Standard deviation'))
    plt.plot(i, c_std, label=('CR Standard deviation'))
    plt.xlabel('Numéro du test')
    plt.ylabel('Statistiques')
    plt.title('Comparaisons des résultats entre PageRank et CheiRank')
    plt.legend(loc='upper right')
    plt.plot()
    plt.show()
