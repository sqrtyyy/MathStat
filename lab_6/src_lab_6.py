import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import scipy.optimize as opt


def add_noize(x: np.ndarray):
    return [x_i + stats.norm.rvs(0, 1) for x_i in x]


def lsm_params(x: np.ndarray, y: np.ndarray):
    beta_1 = np.mean(x * y) - np.mean(x) * np.mean(y)
    beta_0 = np.mean(y) - np.mean(x) * beta_1
    return beta_0, beta_1


def lmm_params(x: np.ndarray, y: np.ndarray):
    beta_0, beta_1 = lsm_params(x, y)
    result = opt.minimize(lambda cur_beta: sum(abs(y[i] - cur_beta[0] - cur_beta[1] * x[i]) for i in range(len(x))),
                          x0=np.asarray([beta_0, beta_1]))
    return result.x[0], result.x[1]


def lsm(x: np.ndarray, y: np.ndarray):
    beta_0, beta_1 = lsm_params(x, y)
    return [beta_0 + beta_1 * x_i for x_i in x]


def lmm(x: np.ndarray, y: np.ndarray):
    beta_0, beta_1 = lmm_params(x, y)
    return [beta_0 + beta_1 * x_i for x_i in x]


def draw(path_to_save: str, name: str, x: np.ndarray, y: np.ndarray, lsm_arr: np.ndarray, lmm_arr: np.ndarray,
         y_ideal: np.ndarray, x_lim: tuple):
    fig, axs = plt.subplots()
    axs.plot(x, y_ideal, color="red", label="Модель")
    axs.plot(x, lsm_arr, color="black", label="МНК")
    axs.plot(x, lmm_arr, color="blue", label="МНМ")
    axs.scatter(x, y, c="black", label="Выборка")
    axs.legend()
    axs.set(title=name)
#    axs.show()

    fig.savefig(path_to_save + name + ".pdf")
