import numpy as np
from matplotlib import pyplot as plt
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg', 'pdf')


def get_qs(sample):
    return np.quantile(sample, [1 / 4, 3 / 4])


def get_xs(q_1, q_3):
    return q_1 - 3 / 2 * (q_3 - q_1), q_3 + 3 / 2 * (q_3 - q_1)


def anomaly_count(sample):
    q_1, q_3 = get_qs(sample)
    x_1, x_2 = get_xs(q_1, q_3)
    count = 0
    for val in sample:
        if val > x_2 or val < x_1:
            count += 1
    return count


def calc_anomaly_percentage(sizes, number_of_calc, sample_gen_function):
    anomaly_percentages = []
    for size in sizes:
        anomalies_number = 0
        for i in range(number_of_calc):
            sample = sample_gen_function(size)
            sample.sort()
            anomalies_number += anomaly_count(sample=sample)
        anomaly_percentages.append(anomalies_number / (size * number_of_calc))
    return anomaly_percentages


def draw_boxplot(sizes, sample_gen_function, name):
    data = []
    plt.show()
    for size in sizes:
        sample = sample_gen_function(size)
        data.append(sample)
    flierprops = dict(marker='.', markerfacecolor='black', markersize=5,
                      markeredgecolor='none')
    plt.boxplot(data, vert=False, labels=sizes, flierprops=flierprops)
    plt.xlabel("x")
    plt.ylabel("n")
    plt.title(name)
    plt.savefig("paper/src/" + name + ".pdf")
    plt.show()

