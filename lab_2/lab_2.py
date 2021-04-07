from math import sqrt

from src_lab_2 import *

samples_sizes = [10, 100, 1000]
N = 1000

gen_sample_functions = [lambda x : np.random.normal(0, 1, x),
                        lambda x : np.random.standard_cauchy(x),
                        lambda x : np.random.laplace(0, 1, x),
                        lambda x : np.random.poisson(10, x),
                        lambda x : np.random.uniform(-sqrt(3), sqrt(3), x)]

path = "paper/src/"
names = ["normal", "cauchy", "laplace", "poisson", "uniform"]
for i in range(len(gen_sample_functions)):
    E_s, D_s = fun(samples_sizes=samples_sizes, number_of_calc=N, sample_gen_function=gen_sample_functions[i])
    for j in range(len(samples_sizes)):
        createLatexTable(path + names[i] + "_" + str(samples_sizes[j]), E_s[j], D_s[j])