import csv
from matplotlib import pyplot as plt
from IPython.display import set_matplotlib_formats

set_matplotlib_formats('svg', 'pdf')


def create_latex_table(table_name: str, angle_elem: str, rows_names: list, columns_names: list, values_matrix,
                       tolerance: int):
    with open(table_name + "_table.tex", "w", newline='') as file:
        writer = csv.writer(file, delimiter='&')
        row = columns_names.copy()
        row.insert(0, angle_elem)
        row[-1] += r"\\ \hline"
        writer.writerow(row)
        for row_number in range(len(rows_names)):
            row = [str(round(val, tolerance)) if isinstance(val, float) else str(val) for val in values_matrix[row_number]]
            row.insert(0, rows_names[row_number])
            row[-1] += r"\\ \hline"
            writer.writerow(row)


def draw_plot_subplots(name: str, titles, xlabels, ylabels, xs, ys, path_to_save: str, styles=None, nrows=1, ncols=1):
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols)
    for i in range(nrows):
        for j in range(ncols):
            idx = i * ncols + j
            ax = axs if nrows + ncols == 2 else axs[idx]
            ax.plot(xs[idx], ys[idx])
            ax.set_xlabel(xlabels[idx])
            ax.set_ylabel(ylabels[idx])
            ax.set(title=titles[idx])
    fig.subplots_adjust(wspace=0.75)
    fig.savefig(path_to_save + name + ".pdf")
    return fig, axs
