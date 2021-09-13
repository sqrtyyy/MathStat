import numpy as np
import scipy.stats as stats
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt


def rQ(sample1: np.asarray, sample2: np.asarray):
    med_1 = np.median(sample1)
    med_2 = np.median(sample2)
    ns = [0, 0, 0, 0]
    size = len(sample1)
    for i in range(size):
        ns[0] = ns[0] + (sample1[i] >= med_1 and sample2 >= med_2)
        ns[1] = ns[1] + (sample1[i] >= med_1 and sample2 <= med_2)
        ns[2] = ns[2] + (sample1[i] <= med_1 and sample2 >= med_2)
        ns[3] = ns[3] + (sample1[i] <= med_1 and sample2 <= med_2)
    return ((ns[0] + ns[2]) - (ns[1] + ns[3])) / size


def get_coefficients(distribution, sample_sizes: list, N: int):
    pearson_coefficients = np.zeros((len(sample_sizes), N))
    quadrant_coefficients = np.zeros((len(sample_sizes), N))
    spearman_coefficients = np.zeros((len(sample_sizes), N))
    for i in range(N):
        samples = [distribution.rvs(size) for size in sample_sizes]
        for j in range(len(sample_sizes)):
            x, y = samples[j][:, 0], samples[j][:, 1]
            pearson_coefficients[j][i] = stats.pearsonr(x, y)[0]
            quadrant_coefficients[j][i] = rQ(x, y)
            spearman_coefficients[j][i] = stats.spearmanr(x, y)[0]
    return pearson_coefficients, quadrant_coefficients, spearman_coefficients

