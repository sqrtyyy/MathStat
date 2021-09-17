import numpy as np
import scipy.stats as stats
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from numba import njit

from IPython.display import set_matplotlib_formats

set_matplotlib_formats('svg', 'pdf')


class MixtureModel(stats.rv_continuous):
    def __init__(self, submodels, coefficients, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submodels = submodels
        self.coefficients = coefficients
        self.dimentions = len(np.array(submodels[0].rvs(1)).shape)

    def _pdf(self, x, **kwargs):
        pdf = self.submodels[0].pdf(x) * self.coefficients[0]
        for i in range(len(self.submodels[1:])):
            pdf += self.submodels[i].pdf(x) * self.coefficients[i]
        return pdf

    def rvs(self, sample_size):
        submodel_choices = np.random.choice(len(self.submodels), size=sample_size, p=self.coefficients)
        submodel_samples = np.array([submodel.rvs(sample_size) for submodel in self.submodels])
        sample = submodel_samples[submodel_choices, np.arange(sample_size), :]
        return sample


#@njit(fastmath=True)
def rQ(sample1: np.ndarray, sample2: np.ndarray) -> float:
    med_1 = np.median(sample1)
    med_2 = np.median(sample2)
    ns = [0, 0, 0, 0]
    size = len(sample1)
    for i in range(size):
        ns[0] = ns[0] + (sample1[i] >= med_1 and sample2[i] >= med_2)
        ns[1] = ns[1] + (sample1[i] <= med_1 and sample2[i] >= med_2)
        ns[2] = ns[2] + (sample1[i] <= med_1 and sample2[i] <= med_2)
        ns[3] = ns[3] + (sample1[i] >= med_1 and sample2[i] <= med_2)
    return ((ns[0] + ns[2]) - (ns[1] + ns[3])) / size


def get_coefficients(distributions: list, sample_size: float, N: int):
    pearson_coefficients = np.zeros((len(distributions), N))
    quadrant_coefficients = np.zeros((len(distributions), N))
    spearman_coefficients = np.zeros((len(distributions), N))
    for i in range(N):
        for j in range(len(distributions)):
            sample = distributions[j].rvs(sample_size)
            x, y = sample[:, 0], sample[:, 1]
            pearson_coefficients[j][i] = stats.pearsonr(x, y)[0]
            quadrant_coefficients[j][i] = rQ(x, y)
            spearman_coefficients[j][i] = stats.spearmanr(x, y)[0]
    return pearson_coefficients, quadrant_coefficients, spearman_coefficients


def help_find_mean(matrix: np.ndarray, rhos: list):
    return [[np.mean(matrix[k]), np.mean(matrix[k] ** 2), np.std(matrix[k]) ** 2] for k in range(len(rhos))]


def eigsorted(cov):
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    return vals[order], vecs[:,order]

def draw_ellipse(path_to_save: str, distribution, title, means, covariation, sample_sizes: list, theoretical=False,
                 fig=None, axs=None):
    nstd = 4
    if fig is None or axs is None:
        fig, axs = plt.subplots(nrows=1, ncols=len(sample_sizes), figsize=(16,4))
    vals_t, vecs_t = eigsorted(covariation)
    theta_t = np.degrees(np.arctan2(*vecs_t[:, 0][::-1]))
    w_t, h_t = nstd * np.sqrt(vals_t)
    for i in range(len(axs)):
        sample = distribution.rvs(sample_sizes[i])
        x, y = sample[:, 0], sample[:, 1]
        ell = None
        if theoretical:
            ell = Ellipse(xy=(means[0], means[1]), width=w_t, height=h_t, angle=theta_t, color='green')
        else:
            cov = np.cov(x, y)
            vals, vecs = eigsorted(cov)
            theta = float(np.degrees(np.arctan2(*vecs[:, 0][::-1])))
            w, h = nstd * np.sqrt(vals)
            ell = Ellipse(xy=(float(np.mean(x)), float(np.mean(y))), width=w, height=h, angle=theta, color='red')
        axs[i].scatter(x, y)
        axs[i].add_artist(ell)
        ell.set_facecolor('none')
        if title:
            axs[i].set(title=title + ", n = " + str(sample_sizes[i]))
        axs[i].set(xlim=(-4, 4))
        axs[i].set(ylim=(-4, 4))

    fig.subplots_adjust(wspace=0.75)
    fig.savefig(path_to_save + ".pdf")
    return fig, axs
