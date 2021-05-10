import csv


def create_latex_table(table_name: str, angle_elem: str, rows_names: list, columns_names: list, values_matrix,
                       tolerance: int):
    with open(table_name + "_table.tex", "w", newline='') as file:
        writer = csv.writer(file, delimiter='&')
        row = columns_names.copy()
        row.insert(0, angle_elem)
        row[-1] += r"\\ \hline"
        writer.writerow(row)
        for row_number in range(len(rows_names)):
            row = [str(round(val, tolerance)) for val in values_matrix[row_number]]
            row.insert(0, rows_names[row_number])
            row[-1] += r"\\ \hline"
            writer.writerow(row)
