import math

import numpy as np
from matplotlib import pyplot as plt


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
    for i in range(num_of_dots):
        t_i[i] = (data[i + 1] - data[i]) / (2 * math.pi)

    ax.set_xlabel('time(ps)')
    ax.scatter(t_i, [1] * num_of_dots, marker='.')
    return t_i


def draw_hist(data: np.array, ax) -> None:
    x, y = [], []
    for element in data:
        x.append(1)
        y.append(element / (2 * math.pi))
    ax.set_xlabel('time')
    ax.hist(y)

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
