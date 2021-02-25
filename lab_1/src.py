import math
import matplotlib.pyplot as plt
import numpy as np


def norm_distribution(x: float, mu: float, sigma: float):
    coeff = 1 / (sigma * math.sqrt(2 * math.pi))
    degree = -((x - mu) ** 2) / (2 * sigma * sigma)
    return coeff * math.exp(degree)


def cauchy_distribution(x: float, x_0: float, gamma: float):
    coeff = 1 / (math.pi * gamma)
    return coeff * 1 / (1 + ((x - x_0) ** 2) / (gamma * gamma))


def laplace_distribution(x, beta, alpha):
    coeff = alpha / 2
    degree = -alpha * math.fabs(x - beta)
    return coeff * math.exp(degree)


def poisson_distribution(k : int, Lambda):
    coeff = (Lambda ** k) / math.factorial(k)
    degree = - Lambda
    return coeff * math.exp(degree)


def uniform_distribution(x, a, b):
    if a <= x <= b:
        return 1 / (b - a)
    return 0


def print_results(sizes, bins_nums, sample_gen_function, distrib_fun, is_discrete=False):
    fig, axs = plt.subplots(len(sizes))
    for i in range(len(sizes)):
        sample = sample_gen_function(sizes[i])
        axs[i].hist(sample, density=True, bins=bins_nums[i])
        if not is_discrete:
            x = np.linspace(min(sample), max(sample))
        else:
            x = np.linspace(min(sample), max(sample), (max(sample) - min(sample)) + 1)
        y = distrib_fun(x)
        axs[i].plot(x, y)
        axs[i].grid()
    plt.show()