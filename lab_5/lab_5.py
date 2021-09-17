import scipy.stats as stats
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt
import src_lab_5 as lab_src
import src

samples_sizes = [20, 60, 100]
N = 1000

path = "paper/src/"
rhos = [0, 0.5, 0.9]

covs = [[[1, rho], [rho, 1]] for rho in rhos]

distributions = [multivariate_normal([0, 0], cov) for cov in covs]

mixed_covs = [
    [[1, 0.9],
     [0.9, 1]],

    [[10, -0.9],
     [-0.9, 10]],
]
mixed_distribution = lab_src.MixtureModel([multivariate_normal([0, 0], mixed_cov) for mixed_cov in mixed_covs],
                                          [0.9, 0.1])

# for i in range(len(samples_sizes)):
#     r, r_q, r_s = lab_src.get_coefficients(distributions=distributions, sample_size=samples_sizes[i], N=N)
#     rows_sub_names = [r"$E(z)$", r"$E(z^2)$", r"$D(z)$", ""]
#     rows_names = [r"$\rho = " + str(rhos[j // 5]) + "$" if j % 5 == 0 else rows_sub_names[j % 5 - 1] for j in
#                   range(1, 14)]
#     columns_names = ['$r$', r"$r_s$", r"$r_Q$"]
#     r_result, r_s_result, r_Q_result = lab_src.help_find_mean(r, rhos), lab_src.help_find_mean(r_s,
#                                                                                                rhos), lab_src.help_find_mean(
#         r_q, rhos)
#     value_matrix = []
#     for j in range(len(rhos)):
#         sub_matrix = []
#         sub_matrix.append(r_result[j])
#         sub_matrix.append(r_s_result[j])
#         sub_matrix.append(r_Q_result[j])
#         sub_matrix = [[sub_matrix[j][i] for j in range(len(sub_matrix))] for i in range(len(sub_matrix[0]))]
#         value_matrix = value_matrix + sub_matrix
#
#     value_matrix.insert(3, [""] * len(columns_names))
#     value_matrix.insert(4, columns_names)
#     value_matrix.insert(8, [""] * len(columns_names))
#     value_matrix.insert(9, columns_names)
#     src.create_latex_table(table_name=path + "CovRhoSampleSize" + str(samples_sizes[i]),
#                            angle_elem=r"$\rho=$" + str(rhos[0]), rows_names=rows_names, columns_names=columns_names,
#                            values_matrix=value_matrix, tolerance=4)
# value_matrix = []
# for i in range(len(samples_sizes)):
#     r, r_q, r_s = lab_src.get_coefficients(distributions=[mixed_distribution], sample_size=samples_sizes[i], N=N)
#     r_result, r_s_result, r_Q_result = lab_src.help_find_mean(r, [0]), lab_src.help_find_mean(r_s, [
#         0]), lab_src.help_find_mean(r_q, [0])
#     sub_matrix = [r_result[0], r_s_result[0], r_Q_result[0]]
#     sub_matrix = [[sub_matrix[j][i] for j in range(len(sub_matrix))] for i in range(len(sub_matrix[0]))]
#     value_matrix = value_matrix + sub_matrix
#
# rows_sub_names = [r"$E(z)$", r"$E(z^2)$", r"$D(z)$", ""]
# rows_names = [r"$n = " + str(samples_sizes[j // 5]) + "$" if j % 5 == 0 else rows_sub_names[j % 5 - 1] for j in
#               range(1, 14)]
# columns_names = ['$r$', r"$r_s$", r"$r_Q$"]
#
# value_matrix.insert(3, [""] * len(columns_names))
# value_matrix.insert(4, columns_names)
# value_matrix.insert(8, [""] * len(columns_names))
# value_matrix.insert(9, columns_names)
#
# src.create_latex_table(table_name=path + "CovMixedSamples",
#                        angle_elem=r"$n=$" + str(samples_sizes[0]), rows_names=rows_names, columns_names=columns_names,
#                        values_matrix=value_matrix, tolerance=4)

titles = ["ρ = 0", "ρ = 0.5", "ρ = 0.9", "Mixed␣two normal"]
for i in range(len(distributions)):
    fig, axs = lab_src.draw_ellipse(distribution=distributions[i], title=titles[i], means=[0, 0], covariation=covs[i],
                                    theoretical=True,
                                    sample_sizes=samples_sizes, path_to_save=path + "RHO_" + str(rhos[i]))

lab_src.draw_ellipse(distribution=mixed_distribution, title=titles[-1], means=[0, 0], covariation=mixed_covs,
                     sample_sizes=samples_sizes, path_to_save=path + "MIXED_ELLIPSE", theoretical=False)
