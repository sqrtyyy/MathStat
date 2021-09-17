import math

import numpy as np
import scipy.stats as stats
import src


def get_intervals(start: float, end: float, sample_size: int):
    k = math.floor(1.72 * (sample_size ** (1 / 3)))
    intervals = np.linspace(start=start, stop=end, num=k - 1)
    intervals = np.insert(intervals, 0, np.NINF)
    intervals = np.append(intervals, np.PINF)
    return k, intervals


def get_probability_and_frequency(sample, distribution, intervals):
    p = []
    n = []
    for i in range(1, len(intervals)):
        p.append(distribution.cdf(intervals[i]) - distribution.cdf(intervals[i - 1]))
        n.append(len(sample[(sample <= intervals[i]) & (sample >= intervals[i - 1])]))
    return np.asarray(p), np.asarray(n)


def calc_chi_addendums(n: np.ndarray, p: np.ndarray, size: int):
    return (size * p - n) ** 2 / (size * p)


def calc_and_save(path, hypothetical_distribution, table_name, interval, size, sample, alpha):
    k, intervals = get_intervals(start=interval[0], end=interval[1], sample_size=size)
    p, n = get_probability_and_frequency(sample=sample, distribution=hypothetical_distribution,
                                         intervals=intervals)
    rows_names = list(np.char.mod('%d', range(1, k + 1)))
    rows_names.append(r"\sum")
    n_i_np_i = n - size * p
    intervals = [[round(intervals[i], 2), round(intervals[i + 1], 2)] for i in range(0, len(intervals) - 1)]
    value_matrix = [intervals, n, p, size * p, n_i_np_i, n_i_np_i * n_i_np_i / (size * p)]
    sums = ["-"] + [sum(value_matrix[i]) for i in range(1, len(value_matrix))]
    value_matrix = [[value_matrix[j][i] for j in range(len(value_matrix))] for i in range(len(value_matrix[0]))]
    value_matrix.append(sums)
    src.create_latex_table(table_name=path + table_name, angle_elem="i", rows_names=rows_names,
                           columns_names=["intervals", r"$n_i$", r"$p_i$", r"$np_i$", r"$n_i - np_i$", r"$\dfrac{(n_i - "
                                                                                               r"np_i)^2}{np_i}$"],
                           values_matrix=value_matrix, tolerance=4)

    f = open(path + "variables.tex", "a")
    f.write(r"\newcommand{\M" + table_name +"ChiRes}{" + str(round(sums[-1], 2)) + "}\n")
    f.close()
