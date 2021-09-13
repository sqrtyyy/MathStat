import math

import numpy as np
import csv


def z_r(sampled_values):
    return (sampled_values[0] + sampled_values[-1]) / 2


def z_p(sampled_values, p):
    np = len(sampled_values) * p
    return sampled_values[int(np)] if int(np) == np else sampled_values[int(np) + 1]


def z_q(sampled_values):
    return (z_p(sampled_values, 1 / 4) + z_p(sampled_values, 3 / 4)) / 2


def z_tr(sampled_values):
    n = len(sampled_values)
    r = int(n / 4)
    sum = 0
    for i in range(r + 1, n - r + 1):
        sum += sampled_values[i]
    return sum / (n - 2 * r)


def fun(samples_sizes, number_of_calc, sample_gen_function):
    E_s = []
    D_s = []
    for samples_size in samples_sizes:
        z_rs = []
        z_qs = []
        z_trs = []
        means = []
        medians = []
        for i in range(number_of_calc):
            sample = sample_gen_function(samples_size)
            sample.sort()
            means.append(np.mean(sample))
            medians.append(np.median(sample))
            z_rs.append(z_r(sample))
            z_qs.append(z_q(sample))
            z_trs.append(z_tr(sample))
        values = [means, medians, z_rs, z_qs, z_trs]
        E_s.append([float(np.mean(value)) for value in values])
        D_s.append([float(np.var(value)) for value in values])
    return E_s, D_s


def estimate(x: float, y: float):
    x_str = str(x)
    y_str = str(y)
    i = 0
    common_str = ""
    while i < len(x_str) and i < len(y_str) and x_str[i] == y_str[i]:
        common_str = common_str + x_str[i]
        i = i + 1
    estimate_str = common_str.split(".")
    if len(estimate_str) != 2:
        return 0
    return len(estimate_str[1])


def createLatexTable(table_name: str, E: list, D : list, tolerance=4):
    with open(table_name + "_table.tex", "w", newline='') as file:
        writer = csv.writer(file, delimiter='&')
        row = [" ", r"$\overline{x}$", r"$med\ x$", "$z_R$", "$z_Q$", r"$z_{tr}$ \\ \hline"]
        writer.writerow(row)
        row = [str(round(val, tolerance)) for val in E]
        row.insert(0, r"$E\left(z\right)$")
        row[-1] = row[-1] + r"\\ \hline"
        writer.writerow(row)
        row = [str(round(val, tolerance)) for val in D]
        row.insert(0, r"$D\left(z\right)$")
        row[-1] += r"\\ \hline"
        writer.writerow(row)
        row = [str(round(E[i] + math.sqrt(D[i]), tolerance)) for i in range(len(list(E)))]
        row.insert(0, r"$E + \sqrt{D}$")
        row[-1] += r"\\ \hline"
        writer.writerow(row)
        row = [str(round(E[i] - math.sqrt(D[i]), tolerance)) for i in range(len(list(E)))]
        row.insert(0, r"$E - \sqrt{D}$")
        row[-1] += r"\\ \hline"
        writer.writerow(row)
        est_arr = [estimate(abs(round(E[i] - math.sqrt(D[i]), tolerance)), round(E[i] + math.sqrt(D[i]), tolerance)) for i in range(len(list(E)))]
        row = [str(int(D[i] * (10 ** est_arr[i])) / (10 ** est_arr[i])) if est_arr[i] != 0 else "-" for i in range(len(est_arr))]
        row.insert(0, r"\widehat{E}(z)")
        row[-1] += r"\\ \hline"
        writer.writerow(row)


if __name__ == "__name__":
    print("hello")
