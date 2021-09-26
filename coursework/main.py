import numpy as np
import matplotlib.pyplot as plt
import math
from tolsolvty import tolsolvty
import cw_src


def getId(val, consts, size):
    if val < consts[0]:
        return 0

    if val > consts[size - 1]:
        return size - 2

    for i in range(size):
        if val > consts[i] and val < consts[i + 1]:
            return i


def getInterpolation(x, y, x_val):
    return y[0] + (x_val - x[0]) / (x[1] - x[0]) * (y[1] - y[0])


def interpolation(data, dc, constants, size, num_const):
    result = np.zeros(size)

    for i in range(size):
        id = getId(data[i], constants[:, i], num_const)
        result[i] = getInterpolation([constants[id, i], constants[id + 1, i]], [dc[id], dc[id + 1]], data[i])

    return result

def get_asin_amp(bin_val, ids):
    dy = 0.001
    di = 1 / 3
    A2_bot = np.zeros((len(ids[1]), 3))
    A2_top = np.zeros((len(ids[1]), 3))
    B2_bot = np.zeros((len(ids[1]), 1))
    B2_top = np.zeros((len(ids[1]), 1))

    A1_bot = np.zeros((len(ids[0]), 3))
    A1_top = np.zeros((len(ids[0]), 3))
    B1_bot = np.zeros((len(ids[0]), 1))
    B1_top = np.zeros((len(ids[0]), 1))

    count = 0

    for i in range(len(ids[0])):
        if i != 0 and ids[0][i] - ids[0][i - 1] > 2:
            count += 1

        A1_bot[i, 0] = ids[0][i] - di + 1
        A1_bot[i, 1] = 1
        A1_bot[i, 2] = count
        B1_bot[i, 0] = bin_val[ids[0][i]] - dy * abs(bin_val[ids[0][i]])

        A1_top[i, 0] = ids[0][i] + di + 1
        A1_top[i, 1] = 1
        A1_top[i, 2] = count
        B1_top[i, 0] = bin_val[ids[0][i]] + dy * abs(bin_val[ids[0][i]])

    count = 0

    for i in range(len(ids[1])):
        if i != 0 and ids[1][i] - ids[1][i - 1] > 2:
            count += 1

        A2_bot[i, 0] = ids[1][i] - di
        A2_bot[i, 1] = 1
        A2_bot[i, 2] = count
        B2_bot[i, 0] = bin_val[ids[1][i]] - dy * abs(bin_val[ids[1][i]])

        A2_top[i, 0] = ids[1][i] + di
        A2_top[i, 1] = 1
        A2_top[i, 2] = count
        B2_top[i, 0] = bin_val[ids[1][i]] + dy * abs(bin_val[ids[1][i]])

    [tolmax, argmax, envs, ccode] = tolsolvty(A1_bot, A1_top, B1_bot, B1_top)
    a1 = argmax[0]
    b1 = argmax[1]
    [tolmax, argmax, envs, ccode] = tolsolvty(A2_bot, A2_top, B2_bot, B2_top)
    a2 = argmax[0]
    b2 = argmax[1]
    y = abs((b1 * a2 - b2 * a1) / (a2 - a1))

    return [y, a1, b1, a2, b2]


def partition(data, size):
    elements = [[], []]

    is_pos = True

    if data[0] < data[1]:
        is_pos = True
        elements[0].append(0)
    else:
        is_pos = False
        elements[1].append(0)

    for i in range(1, size):
        if data[i] >= data[i - 1]:
            elements[0].append(i)
        else:
            elements[1].append(i)

    return elements


def scale(data, size, ampl):
    result = []

    coef = math.pi / (2 * ampl)

    for i in range(size):
        result.append(data[i] * coef)

    return result


path = "paper/src/"

data_src_dir = 'data'

signal_id = 14
signal_path = '/Sin_100MHz/sin_100MHz_'
path_minus_0_5 = '/-0_5V/-0_5V_'
path_minus_0_25 = '/-0_25V/-0_25V_'
path_zero = '/ZeroLine/ZeroLine_'
path_plus_0_25 = '/+0_25V/+0_25V_'
path_plus_0_5 = '/+0_5V/+0_5V_'

color1 = 'b'
color2 = 'r'
color3 = 'c'
color4 = 'g'
color5 = 'm'
color6 = 'y'

data1 = cw_src.read_file(data_src_dir + signal_path + str(signal_id) + ".txt", array_size=1024)
all_data = cw_src.read_files_in_dir(data_src_dir + signal_path, array_size=1024, num_of_files=100)
data2 = cw_src.read_files_in_dir(data_src_dir + path_minus_0_5, array_size=1024, num_of_files=100)
data3 = cw_src.read_files_in_dir(data_src_dir + path_minus_0_25, array_size=1024, num_of_files=100)
data4 = cw_src.read_files_in_dir(data_src_dir + path_zero, array_size=1024, num_of_files=100)
data5 = cw_src.read_files_in_dir(data_src_dir + path_plus_0_25, array_size=1024, num_of_files=100)
data6 = cw_src.read_files_in_dir(data_src_dir + path_plus_0_5, array_size=1024, num_of_files=100)

data1 = np.mean(data1, axis=1)
all_data = cw_src.average_data(data=all_data)
data2 = cw_src.average_data(data=data2)
data3 = cw_src.average_data(data=data3)
data4 = cw_src.average_data(data=data4)
data5 = cw_src.average_data(data=data5)
data6 = cw_src.average_data(data=data6)

fig, ax = cw_src.draw_amplitudes(data1, color1)
cw_src.draw_amplitudes(data2, color2, fig=fig, ax=ax)
cw_src.draw_amplitudes(data3, color3, fig=fig, ax=ax)
cw_src.draw_amplitudes(data4, color4, fig=fig, ax=ax)
cw_src.draw_amplitudes(data5, color5, fig=fig, ax=ax)
cw_src.draw_amplitudes(data6, color6, fig=fig, ax=ax)

fig.savefig(path + "AmplitudeValues" + ".pdf")

cw_src.draw_amplitudes(data1, color1, fig=fig, ax=ax)
fig.savefig(path + "AmplitudeValuesWithSignals" + ".pdf")

dc = [-0.5, -0.25, 0.0, 0.25, 0.5]
constants = np.array([data2, data3, data4, data5, data6])

data1 = interpolation(data1, dc, constants, len(data1), len(constants))
all_data = interpolation(all_data, dc, constants, len(data1), len(constants))
fig, ax = cw_src.draw_amplitudes(data1, color1)
fig.savefig(path + "InterpolatedSignal" + ".pdf")

sin_data = np.divide(data1, max(abs(max(data1)), abs(min(data1))))
sin_data = np.add(sin_data, 1)
sin_data = np.divide(sin_data, max(sin_data))

all_data = np.divide(all_data, max(abs(max(all_data)), abs(min(all_data))))
all_data = np.add(all_data, 1)
all_data = np.divide(all_data, max(all_data))
#all_data = np.arcsin(all_data)


data1 = sin_data

fig, ax = cw_src.draw_amplitudes(sin_data, color1)
fig.savefig(path + "Signal[0,1]" + ".pdf")

sin_data = np.arcsin(sin_data)

fig, ax = cw_src.draw_amplitudes(sin_data, color1)
fig.savefig(path + "ScaledSignal" + ".pdf")

elements = partition(sin_data, len(data1))
[ampl, a1, b1, a2, b2] = get_asin_amp(sin_data, elements)

cw_src.draw_arcsin_lines(a1, b1, a2, b2, ax, 50)

fig.savefig(path + "ArcsinParams" + ".pdf")

data1 = cw_src.set_amplitude(data1, ampl)
all_data =cw_src.set_amplitude(all_data, ampl)

fig, ax = plt.subplots()
x_i = cw_src.draw_delta_times(data=data1, num_of_dots=40, ax=ax)
fig.savefig(path + "TimePeriods" + ".pdf")

fig, ax = plt.subplots()
cw_src.draw_hist(data=all_data, ax=ax)
fig.savefig(path + "TimeHistogram" + ".pdf")

