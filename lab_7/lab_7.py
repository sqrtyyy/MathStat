import math

import numpy as np
import scipy.stats as stats
import src_lab_7 as lab_src
import src

N = 100
interval = [-1.1, 1.1]
path = "paper/src/"
alpha = 0.05

real_distribution = stats.norm().rvs(N)

f = open(path + "variables.tex", "w")
f.write(r"\newcommand{\REALMU}{" + str(round(np.mean(real_distribution), 4)) + "}\n")
f.write(r"\newcommand{\REALSIGMA}{" + str(round(np.std(real_distribution), 4)) + "}\n")
f.close()

hypothetical_distributions = [stats.norm(), stats.laplace(),
                              stats.uniform(loc=interval[0] - 1, scale=(interval[1] - interval[0]) + 2)]
hypothetical_distributions_names = ["NORMAL", "LAPLACE", "UNIFORM"]

sample = stats.norm().rvs(N)

lab_src.calc_and_save(hypothetical_distribution=hypothetical_distributions[0], table_name="RealDistribution",
                      interval=interval, size=N, sample=sample, path=path, alpha=0.05)

f = open(path + "variables.tex", "a")
k = math.floor(1.72 * (N ** (1 / 3)))
f.write(r"\newcommand{\BigNK}{" + str(k) + "}\n")
f.write(r"\newcommand{\LevelAlpha}{" + str(alpha) + "}\n")
f.write(r"\newcommand{\BigChi}{" + str(round(stats.chi2.ppf(1 - alpha, k - 1), 2)) + "}\n")
f.close()

N_1 = 20
sample = stats.norm().rvs(N_1)

for i in range(1, len(hypothetical_distributions)):
    lab_src.calc_and_save(hypothetical_distribution=hypothetical_distributions[i],
                          table_name=hypothetical_distributions_names[i], interval=interval, size=N_1,
                          sample=sample, path=path, alpha=0.05)

f = open(path + "variables.tex", "a")
k = math.floor(1.72 * (N_1 ** (1 / 3)))
f.write(r"\newcommand{\SmallNK}{" + str(k) + "}\n")
f.write(r"\newcommand{\SmallChi}{" + str(round(stats.chi2.ppf(1 - alpha, k - 1), 2)) + "}\n")
f.close()
