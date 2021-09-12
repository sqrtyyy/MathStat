from math import sqrt

import numpy as np

from src_lab_4 import *
from scipy import stats

sample_sizes = [20, 60, 100]
distributions = [stats.norm(), stats.cauchy(0, 1), stats.laplace(0, 1 / sqrt(2)), stats.poisson(10),
                 stats.uniform(loc=-sqrt(3), scale=2 * sqrt(3))]
names = ["normal", "cauchy", "laplace", "poisson", "uniform"]
path = "paper/src/"
grid_continuous = np.linspace(-4, 4, 50)
grid_discreet = np.linspace(6, 14, 50)
coefficients = [0.5, 1, 2]
grids = [grid_continuous, grid_continuous, grid_continuous, grid_discreet, grid_continuous]
for i in range(len(distributions)):
    #draw_empirical_function(distribution=distributions[i],sizes=sample_sizes, grid=grids[i],name=names[i], path_to_save=path)
    draw_kde(distribution=distributions[i], grid=grids[i], name=names[i], path_to_save=path, sizes=sample_sizes, coeffs=coefficients)


