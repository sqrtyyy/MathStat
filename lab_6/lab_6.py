import src_lab_6 as src
import numpy as np

from IPython.display import set_matplotlib_formats

set_matplotlib_formats('svg', 'pdf')

x = np.arange(-1.8, 2, 0.2)
y_ideal = 2 + 2 * x
x_lim = (-1.8, 2)

y = src.add_noize(y_ideal)

path = "paper/src/"

lsm = src.lsm(x, y)
lmm = src.lmm(x, y)
src.draw(path_to_save=path, name="Without Perturbations", x=x, y=y, lsm_arr=lsm, lmm_arr=lmm, y_ideal=y_ideal,
         x_lim=x_lim)

lsm_dist = sum((y_ideal[i] - lsm[i]) ** 2 for i in range(len(y)))
lmm_dist = sum(abs(y_ideal[i] - lmm[i]) for i in range(len(y)))

f = open(path + "variables.tex", "w")
f.write(r"\newcommand{\WithoutPertLSMBetaNULL}{" + str(round(src.lsm_params(x, y)[0], 2)) + "}\n")
f.write(r"\newcommand{\WithoutPertLSMBetaONE}{" + str(round(src.lsm_params(x, y)[1], 2)) + "}\n")
f.write(r"\newcommand{\WithoutPertLMMBetaNULL}{" + str(round(src.lmm_params(x, y)[0], 2)) + "}\n")
f.write(r"\newcommand{\WithoutPertLMMBetaONE}{" + str(round(src.lmm_params(x, y)[1], 2)) + "}\n")
f.write(r"\newcommand{\WithoutPertLSMDistance}{" + str(round(lsm_dist, 2)) + "}\n")
f.write(r"\newcommand{\WithoutPertLMMDistance}{" + str(round(lmm_dist, 2)) + "}\n")
f.close()

y[0] += 10
y[-1] -= 10
lsm = src.lsm(x, y)
lmm = src.lmm(x, y)
src.draw(path_to_save=path, name="With Perturbations", x=x, y=y, lsm_arr=lsm, lmm_arr=lmm, y_ideal=y_ideal, x_lim=x_lim)

lsm_dist = sum((y_ideal[i] - lsm[i]) ** 2 for i in range(len(y)))
lmm_dist = sum(abs(y_ideal[i] - lmm[i]) for i in range(len(y)))

f = open(path + "variables.tex", "a")
f.write(r"\newcommand{\WithPertLSMBetaNULL}{" + str(round(src.lsm_params(x, y)[0], 2)) + "}\n")
f.write(r"\newcommand{\WithPertLSMBetaONE}{" + str(round(src.lsm_params(x, y)[1], 2)) + "}\n")
f.write(r"\newcommand{\WithPertLMMBetaNULL}{" + str(round(src.lmm_params(x, y)[0], 2)) + "}\n")
f.write(r"\newcommand{\WithPertLMMBetaONE}{" + str(round(src.lmm_params(x, y)[1], 2)) + "}\n")
f.write(r"\newcommand{\WithPertLSMDistance}{" + str(round(lsm_dist, 2)) + "}\n")
f.write(r"\newcommand{\WithPertLMMDistance}{" + str(round(lmm_dist, 2)) + "}\n")
f.close()
