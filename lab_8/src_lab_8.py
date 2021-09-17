import math
from enum import Enum

import numpy as np
import matplotlib.pyplot as plt
from IPython.display import set_matplotlib_formats

set_matplotlib_formats('svg', 'pdf')


class SignalType(Enum):
    SIGNAL = "Сигнал"
    BACKGROUND = "Фон"
    TRANSFER = "Переход"

    def __str__(self):
        return self.value


def read_signal(filename: str, one_signal_size: int) -> np.ndarray:
    data: list
    with open(filename, 'r') as f:
        data = [[float(item) for item in line.replace("[", "").replace("]", "").split(", ")] for line in f]
    return np.reshape(data, (len(data[0]) // one_signal_size, one_signal_size))


def s_inter_group(x: np.ndarray) -> float:
    x_i_mean = np.asarray([np.mean(x_i) for x_i in x])
    x_mean = float(np.mean(x_i_mean))
    sum = 0
    for x_i_m in x_i_mean:
        sum += (x_i_m - x_mean) ** 2

    return x.shape[0] * sum / (x.shape[0] - 1)


def s_intra_group(x: np.ndarray) -> float:
    sum = 0
    for x_i in x:
        x_mean = np.mean(x_i)
        tmp_sum = 0
        for x_i_j in x_i:
            tmp_sum += (x_i_j - x_mean) ** 2
        sum = sum + tmp_sum / x.shape[0]

    return sum / x.shape[0]


def fisher_criteria(sample: np.ndarray, k: int) -> tuple:
    n = len(sample)
    newSizeY = int(n / k)
    newSizeX = k
    groups = np.reshape(sample, (newSizeX, newSizeY))
    inter = s_inter_group(groups)
    intra = s_intra_group(groups)
    return inter / intra, inter, intra


def get_k(num: int) -> int:
    k = 4
    while num % k != 0:
        k += 1
    return k


def get_hist(sample, intervals) -> np.ndarray:
    return np.array([len(sample[np.logical_and(sample >= intervals[i], sample < intervals[i + 1])]) for i in
                     range(intervals.size - 1)])


def save_hist(path_to_save: str, name: str, title: str, sample: np.ndarray, num_bins: int) -> None:
    fig, ax = plt.subplots()
    ax.hist(sample, num_bins)
    ax.set(title=title)
    fig.savefig(path_to_save + name + ".pdf")


def get_intervals_types(sample: np.ndarray, num_bins: int) -> tuple:
    intervals = np.linspace(min(sample), max(sample), num_bins + 1)
    hist = get_hist(sample=sample, intervals=intervals)
    sorted_hist = sorted(hist)
    types = []
    for i in range(num_bins):
        types.append(
            SignalType.BACKGROUND if hist[i] == sorted_hist[-1] else
            SignalType.SIGNAL if hist[i] == sorted_hist[-2] else
            SignalType.TRANSFER)
    return types, intervals


def convert(signal: np.ndarray, intervals: np.ndarray, types: list) -> tuple:
    p_type = [0] * len(signal)
    zones = []
    areas_type = []
    for i in range(len(signal)):
        for j in range(len(types)):
            if (signal[i] >= intervals[j]) and (signal[i] <= intervals[j + 1]):
                p_type[i] = types[j]
    currType = p_type[0]
    start = 0
    finish = 0
    for i in range(len(p_type)):
        if currType != p_type[i]:
            finish = i
            areas_type.append(currType)
            zones.append([start, finish])
            start = finish
            currType = p_type[i]
    if currType != areas_type[len(areas_type) - 1]:
        areas_type.append(currType)
        zones.append([finish, - 1])
    return zones, areas_type


def save_segmented(signal: np.ndarray, intervals: list, types: list, title: str, path_to_save: str, name: str) -> None:
    fig, ax = plt.subplots()
    indexes = range(signal.size)
    for i in range(len(intervals)):
        color_ = ""
        if types[i] == SignalType.BACKGROUND:
            color_ = 'y'
        if types[i] == SignalType.SIGNAL:
            color_ = 'r'
        if types[i] == SignalType.TRANSFER:
            color_ = 'g'
        ax.plot(indexes[intervals[i][0]:intervals[i][1]], signal[intervals[i][0]:intervals[i][1]],
                color=color_, label=types[i])
    ax.legend()
    ax.set(title=title)
    fig.savefig(path_to_save + name + ".pdf")
    plt.show()


def fisher(signal: np.ndarray, area_data):
    fishers = []
    k_arr = []
    s_1_arr = []
    s_2_arr = []
    zs = [area_data[0], area_data[1], [area_data[2][0], area_data[-3][1]], area_data[-2], area_data[-1]]
    for i in range(len(zs)):
        start = zs[i][0]
        finish = zs[i][1]
        k = get_k(finish - start)
        while k == finish - start:
            finish += 1
            k = get_k(finish - start)
        f, s_1, s_2 = fisher_criteria(signal[start:finish], k)
        fishers.append(f)
        k_arr.append(k)
        s_1_arr.append(s_1)
        s_2_arr.append(s_2)
    return k_arr, s_1_arr, s_2_arr, fishers
