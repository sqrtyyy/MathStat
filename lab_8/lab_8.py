import src_lab_8 as lab_src
import src

signal_id = 500
N = 25
path = "paper/src/"

file_data = lab_src.read_signal("data/wave_ampl.txt", 1024)
signal = file_data[signal_id]

src.draw_plot_subplots(name=f"Signal{signal_id}", titles=[f"Signal = {signal_id}"], xlabels=[""], ylabels=[""],
                       xs=[range(len(signal))], ys=[signal], path_to_save=path)

lab_src.save_hist(path_to_save=path, name=f"Signal{signal_id}Hist", title="Signal histogram", num_bins=N, sample=signal)

types, intervals = lab_src.get_intervals_types(sample=signal, num_bins=N)
zones, areas_type = lab_src.convert(signal, intervals, types)
lab_src.save_segmented(signal=signal, types=areas_type, intervals=zones, title="Segmented areas",
                       path_to_save=path, name=f"Segmented{signal_id}")

k_arr, s_1_arr, s_2_arr, fishers = lab_src.fisher(signal, zones)

values_matrix = [areas_type, k_arr, fishers]
values_matrix = [[values_matrix[j][i] for j in range(len(values_matrix))] for i in range(len(values_matrix[0]))]
src.create_latex_table(table_name=path + "Fisher", angle_elem="Промежуток", rows_names=list(range(1, len(k_arr) + 1)),
                       columns_names=["Тип","Количество разбиений", "Критерий Фишера"], values_matrix=values_matrix,
                       tolerance=4)

