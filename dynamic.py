import random
import matplotlib.pyplot as plt
import numpy as np

n_simulations = 100

# in this version, the sizes of 3 sets are allowed to be different.

def sample_fixed_sum(sigma, n):
    """sample n integers which sum to sigma"""
    res = [np.random.randint(0, sigma)]
    part_sum = res[0]
    for i in range(1,n-1):
        res.append(np.random.randint(0, sigma - part_sum))
        part_sum += res[-1]
    res.append(sigma - part_sum)
    return res

def sample_sets(size_0=20, size_L=40, size_R=60):
    """does this algorithm admit unbiased distribution (each possible config has same probability)?"""
    # according to figure 10
    # first sample C C = np.random.randint(0, min(size_0, size_L, size_R))
    # then sample B,D,F
    B = np.random.randint(0, min(size_0 - C, size_L - C))
    D = np.random.randint(0, min(size_0 - B - C, size_R - C))
    F = np.random.randint(0, min(size_L - B - C, size_R - D - C))
    # then compute A, E, G
    A = size_0 - B - C - D
    E = size_L - B - C - F
    G = size_R - C - D - F

    return A,B,C,D,E,F,G



for i in range(n_simulations):
    size_0 = 892
    size_L = 892
    size_R = 892

    A,B,C,D,E,F,G = sample_sets(size_0, size_L, size_R)
    eL = A + D
    aL = E + F
    eR = A + B
    aR = F + G

    bigunion = A+B+C+D+E+F+G
    bound102 = 2/3*size_L + 2/3*size_R - bigunion
    bound103 = size_L/3 - (2/3*aL + 2/3*eR + aR/3 + eL/3)
    print(bound102, bound103)

    # lemma 10.2: if B_L and B_R are finalized, is this necessary that the intersection of their attestation sets > 0?
    



