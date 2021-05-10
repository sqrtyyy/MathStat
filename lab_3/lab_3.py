from math import sqrt
from src import create_latex_table
from src_lab_3 import *
from lab_1 import src_lab_1
from scipy import stats

samples_sizes = [20, 100]
N = 1000

gen_sample_functions = [lambda x : np.random.normal(0, 1, x),
                        lambda x : np.random.standard_cauchy(x),
                        lambda x : np.random.laplace(0, 1, x),
                        lambda x : np.random.poisson(10, x),
                        lambda x : np.random.uniform(-sqrt(3), sqrt(3), x)]
distrib_functions = [lambda x : src_lab_1.norm_distribution(x, 0, 1),
                     lambda x : src_lab_1.cauchy_distribution(x, 0, 1),
                     lambda x : src_lab_1.laplace_distribution(x, 0, 1 / sqrt(2)),
                     lambda k : src_lab_1.poisson_distribution(k, 10),
                     lambda x : src_lab_1.uniform_distribution(x, -sqrt(3), sqrt(3))]
is_discreet          = [False,
                        False,
                        False,
                        True,
                        False]
names = ["normal", "cauchy", "laplace", "poisson", "uniform"]
path = "paper/src/"
i = 0
anomalies = []
for gen_sample_function in gen_sample_functions:
    anomalies.append(calc_anomaly_percentage(sizes= samples_sizes, number_of_calc= N, sample_gen_function=gen_sample_function))
    draw_boxplot(sizes=samples_sizes, sample_gen_function=gen_sample_function, name=names[i])
    i += 1
create_latex_table(table_name=path + "experimental_anomaly",angle_elem="sample size",rows_names=names,columns_names=[str(size) for  size in samples_sizes], values_matrix=anomalies, tolerance=3)

q_1_t = []
q_3_t = []
x_1_t = []
x_2_t = []
P_o_t = []
distributions = [stats.norm(), stats.cauchy(0, 1), stats.laplace(0, 1/ sqrt(2)), stats.poisson(10), stats.uniform(loc=-sqrt(3),
                                                                                                                  scale=2 * sqrt(3))]
for j in range(len(distributions)):
    rv = distributions[j]
    q_1_t.append(rv.ppf(1 / 4))
    q_3_t.append(rv.ppf(3 / 4))
    x_1, x_2 = get_xs(q_1_t[-1], q_3_t[-1])
    x_1_t.append(x_1)
    x_2_t.append(x_2)
    if is_discreet[j]:
        P_o_t.append(rv.cdf(x_1) - rv.pmf(x_1) + (1 - rv.cdf(x_2)))
    else:
        P_o_t.append(rv.cdf(x_1) + (1 - rv.cdf(x_2)))
results = np.array([q_1_t, q_3_t, x_1_t, x_2_t, P_o_t])
results = results.T
names_2 = [r"$Q^{T}_{1}$", r"$Q^{T}_{3}$", r"$X^{T}_{1}$", r"$X^{T}_{2}$", r"$P^{T}_{B}$"]
create_latex_table(table_name=path + "theoretical_anomaly", angle_elem="",rows_names=names,columns_names=names_2,
                   values_matrix=results, tolerance=3)
