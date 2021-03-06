import numpy as np

def z_r(sampled_values):
    return (sampled_values[0] + sampled_values[-1]) / 2


def z_p(sampled_values, p):
    np = len(sampled_values) * p
    return sampled_values[np] if int(np) == np else sampled_values[int(np) + 1]


def z_q(sampled_values):
    return (z_p(sampled_values, 1 / 4) + z_p(sampled_values, 3 / 4)) / 2


def z_tr(sampled_values):
    n = len(sampled_values)
    r = int(n / 4)
    return sum(sampled_values[r + 1: n - r]) / (n - 2 * r)

def fun(samples_sizes, number_of_calc):
    for samples_size in samples_sizes:


if __name__ == "__name__":
    print("hello")

