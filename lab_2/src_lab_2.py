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
    return sum(sampled_values[r + 1: n - r]) / (n - 2 * r)


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
        E_s.append(np.mean(value) for value in values)
        D_s.append(np.var(value) for value in values)
    return E_s,D_s


def createLatexTable(table_name: str, E, D , tolerance = 4):
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


if __name__ == "__name__":
    print("hello")
