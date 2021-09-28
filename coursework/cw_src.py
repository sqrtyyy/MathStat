import math

import numpy as np
from matplotlib import pyplot as plt
import scipy.optimize as opt
from numba import njit


def read_file(file_name: str, array_size: int) -> np.array:
    with open(file_name, 'r') as f:
        s1 = f.readline().replace("STOP Position =  ", "")
        num = int(s1)
        result = np.zeros((array_size, 9))
        for i in range(array_size):
            s1 = f.readline()
            s1 = s1.replace("\n", "")
            s1 = s1.split('   ')
            array = [float(s1[j]) for j in range(1, len(s1) - 1)]
            result[(array_size + i - num) % array_size] = array
    return result


def read_files_in_dir(dir_name: str, num_of_files: int, array_size: int) -> np.array:
    data = np.zeros((num_of_files, array_size, 9))
    for i in range(num_of_files):
        data[i] = read_file(file_name=dir_name + str(i) + ".txt", array_size=array_size)
    return data


def average_data(data: np.array) -> np.array:
    data = np.mean(data, axis=2)
    result = np.mean(data, axis=0)

    return result


def draw_amplitudes(data: np.array, color: str, fig=None, ax=None):
    if not fig or not ax:
        fig, ax = plt.subplots()
    ax.plot(range(data.size), data, color=color)

    ax.set_xlabel("Time bin")
    ax.set_ylabel("Amplitude value")

    return fig, ax


def set_amplitude(data: np.array, coefficient: float) -> np.array:
    new_data = np.divide(data, max(abs(max(data)), abs(min(data))))
    return np.multiply(new_data, coefficient)


def draw_arcsin_lines(a1: float, b1: float, a2: float, b2: float, ax, num_of_dots: int) -> None:
    x = np.zeros(num_of_dots)
    y1 = np.zeros(num_of_dots)
    y2 = np.zeros(num_of_dots)
    for i in range(num_of_dots):
        x[i] = i
        y1[i] = a1 * x[i] + b1
        y2[i] = a2 * x[i] + b2

    ax.plot(x, y1, 'g')
    ax.plot(x, y2, 'r')


def draw_delta_times(data: np.array, num_of_dots: int, ax) -> np.array:
    t_i = np.zeros(num_of_dots)
    for i in range(1, num_of_dots):
        t_i[i] = t_i[i - 1] + abs(data[i] - data[i + 1]) / (2 * 100 * 10**6 * math.pi)
   # t_i = np.add(t_i, abs(min(t_i)))
    ax.set_xlabel('time(s)')
    ax.scatter(t_i, [1] * num_of_dots, marker='.')
    return t_i


def draw_hist(data: np.array, ax) -> None:
    y = []
    for element in data:
        y.append(element / (2 * 100 * 10**6 * math.pi))
    ax.set_xlabel('time(s)')
    ax.hist(y, bins=16)

def restore_fun(data: np.array, x_i: np.array, tolerance: float):
    def D_M(x: float) -> float:
        return math.sin((2 * M + 1) * math.pi * x) / math.sin(math.pi * x + 0.000001)

    def w_i(i: int) -> float:
        return (x_i[i + 1] - x_i[i - 1]) / 2

    delta = np.NINF

    for i in range(1, x_i.size):
        delta = max(delta, x_i[i] - x_i[i - 1])

    M = delta / 2
    alpha = (2 / (1 + 2 * delta * M) ** 2) / 2
    p_0 = lambda x: alpha * sum([data[i] * w_i(i) * D_M(x - x_i[i])
                                 for i in range(1, x_i.size - 1)])

    p_n = lambda x: p_0(x) + alpha * sum([(data[i] - p_0(x_i[i])) * w_i(i) * D_M(x - x_i[i])
                                          for i in range(1, x_i.size - 1)])

    while math.isclose(p_n(x_i[10]), p_0(x_i[10]), abs_tol=tolerance):
        p_n_1 = p_0
        p_0 = p_n
        p_n = lambda x: p_0(x) + alpha * sum([(data[i] - p_n_1(x_i[i])) * w_i(i) * D_M(x - x_i[i])
                                              for i in range(1, x_i.size - 1)])

    return p_n


def lsm_params(x: np.array, y: np.ndarray):
    beta_1 = np.mean(x * y) - np.mean(x) * np.mean(y)
    beta_0 = np.mean(y) - np.mean(x) * beta_1
    return beta_0, beta_1

def lmm_params(x: np.ndarray, y: np.ndarray) -> tuple:
    beta_0, beta_1 = lsm_params(x, y)
    result = opt.minimize(lambda cur_beta: sum(abs(y[i] - cur_beta[0] - cur_beta[1] * x[i]) for i in range(len(x))),
                          x0=np.asarray([beta_0, beta_1]))
    return result.x[0], result.x[1]


# def get_coeffs(x : np.array, y : np.array):
#     return lsm_params(x, y)
def get_coeffs(constants: np.ndarray, datas: np.ndarray):
    a = np.zeros(datas.shape[1])
    b = np.zeros(datas.shape[1])
    for i in range(datas.shape[1]):
        y = datas[..., i]
        b[i], a[i] = lmm_params(constants, y)
    return a, b


def interpolate(constants: np.array, datas: np.array, signal: np.array, ax):
    a, b = get_coeffs(constants=constants, datas=datas)
    ax.scatter(constants, [datas[i][10] for i in range(datas.shape[0])], marker = '.', color= "r")
    x = np.linspace(min(constants), max(constants), 100)
    y = a[10] * x + b[10]
    ax.plot(x, y)
    ax.set_xlabel("constants")
    ax.set_ylabel("y")
    return np.arcsin((signal - b) / a)
