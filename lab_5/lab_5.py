import numpy as np
import scipy.stats as stats
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt

samples_sizes = [20, 60, 100]
N = 1000

covs = [
    [[1, 0],
     [0, 1]],

    [[1, 0.5],
     [0.5, 1]],

    [[1, 0.9],
     [0.9, 1]],
]

distributions = [multivariate_normal([0, 0], cov) for cov in covs]

mixed_covs = [
    [[1, 0.9],
     [0.9, 1]],

    [[10, -0.9],
     [-0.9, 10]],
]

mixed_distribution = 0.9 * stats.multivariate_normal.rvs([0, 0], mixed_covs[0]) + 0.1 * stats.multivariate_normal.rvs([0, 0], mixed_covs[1])
