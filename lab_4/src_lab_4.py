from scipy import stats

from src import *


def get_empirical_function(sample, grid):
    result = []
    n = len(sample)
    for x in grid:
        result.append(len(sample[sample < x]) / n)
    return result


def draw_empirical_function(distribution, sizes, grid, name, path_to_save):
    samples = [distribution.rvs(size) for size in sizes]
    fig, axs = draw_plot_subplots(name="emperical_fun_" + name,
                                  titles=[name + " n = {}".format(size) for size in sizes],
                                  xlabels=["x"] * 3, ylabels=["F(x)"] * 3,
                                  xs=[grid] * 3,
                                  ys=[get_empirical_function(sample=sample, grid=grid) for sample in samples],
                                  path_to_save=path_to_save, ncols=3)
    for i in range(len(sizes)):
        axs[i].plot(grid, distribution.cdf(grid), "g")

    fig.savefig(path_to_save + "emperical_fun_" + name + ".pdf")
    plt.show()


def get_kde(sample, x_i, coefficient):
    kde = stats.gaussian_kde(sample)
    kde.set_bandwidth(bw_method='silverman')
    kde.set_bandwidth(bw_method=kde.factor * coefficient)
    return kde(x_i)


def draw_kde(distribution, sizes, grid, name, path_to_save, coeffs):
    samples = [distribution.rvs(size) for size in sizes]

    if name != "poisson":
        y = [distribution.pdf(grid)] * len(coeffs)
    else:
        y = [stats.poisson.pmf(10, grid)] * len(coeffs)

    for i in range(len(sizes)):
        fig, axs = draw_plot_subplots(name="kde_{}_".format(sizes[i]) + name,
                                      titles=[name + " n = {}\n h_n / 2".format(sizes[i]),
                                              name + " n = {}\n h_n".format(sizes[i]),
                                              name + " n = {}\n 2 * h_n".format(sizes[i])],
                                      xlabels=["x"] * 3, ylabels=["f(x)"] * 3,
                                      xs=[grid] * 3,
                                      ys=y,
                                      path_to_save=path_to_save, ncols=3)
        for j in range(len(coeffs)):
            axs[j].plot(grid, get_kde(sample=samples[i], x_i=grid, coefficient=coeffs[j]), "g")
        fig.savefig(path_to_save + "kde_{}_".format(sizes[i]) + name + ".pdf")
        plt.show()
