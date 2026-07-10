import instrument as ins
import measurement as ms
import numpy as np
import pandas as pd

common_name = 'name'

ref_path = ms.ref_path
pulse_voltage_range = np.arange(5.0, 4.5, -0.5)
pulse_width_arr = np.arange(40, 45, 5)
array1 = np.arange(0,10,5)
array2 = np.append(array1, np.arange(10,35, 5))

trailing_edge_setup = array2
leading_edge_setup = array2
low_voltage_set = 0

#1. trailing edge sweep
for v in pulse_voltage_range:
    pulse_voltage = v
    folder_name = f'{common_name}_{pulse_voltage}V'
    ms.saving_folder(ref_path, folder_name)

    for a in pulse_width_arr:
        pulse_width_label = round(a, 3)
        folder_name_1 = f'{pulse_width_label} us'
        ms.saving_folder(ref_path + folder_name + r'\\', folder_name_1)
        pulse_width = pulse_width_label * 1E-6
        low = low_voltage_set

        EL_intensity_trailing = pd.DataFrame()
        pulse_data_trailing = pd.DataFrame()
        normalized_data_trailing = pd.DataFrame()

        for x in trailing_edge_setup:
            scope = ins.scope_connection()
            func_gen = ins.func_gen_connection()
            trailing_width_label = round(x, 3)
            i = x * 1E-6
            ins.func_gen_setting_edge_modify(func_gen, pulse_width, pulse_voltage, low, i)
            ins.func_gen_output(func_gen)
            ins.scope_setting_edge(scope, pulse_width, pulse_voltage, low)
            data = ms.data_measure(scope)
            n_data = ms.data_slicing(data)
            n_x = n_data[0]
            n_y1 = n_data[1]  # pulse data
            n_y2 = n_data[2]  # y2가 EL intensity
            ins.func_gen_off(func_gen)
            ins.scope_off(scope)

            EL_intensity_trailing['Time (us)'] = n_x
            EL_intensity_trailing[f'EL intensity_{trailing_width_label}us'] = n_y2
            pulse_data_trailing['Time (us)'] = n_x
            pulse_data_trailing[f'pulse_{trailing_width_label}us'] = n_y1
            normalized_data_trailing['Time (us)'] = n_x
            normalization = (n_y2 - min(n_y2)) / (max(n_y2) - min(n_y2))
            normalized_data_trailing[f'EL normalized_{trailing_width_label}us'] = normalization
            EL_intensity_trailing.to_csv(
                f'Trailing 1. EL intensity {pulse_voltage}V {pulse_width_label}us.csv')
            pulse_data_trailing.to_csv(
                f'Trailing 2. pulse {pulse_voltage}V {pulse_width_label}us.csv')
            normalized_data_trailing.to_csv(
                f'Trailing 3. normalized data {pulse_voltage}V {pulse_width_label}us.csv')


        #leading edge sweep

        pulse_width_label = round(a, 3)
        folder_name_1 = f'{pulse_width_label} us'
        ms.saving_folder(ref_path + folder_name + r'\\', folder_name_1)
        pulse_width = pulse_width_label * 1E-6
        low = low_voltage_set

        EL_intensity_leading = pd.DataFrame()
        pulse_data_leading = pd.DataFrame()
        normalized_data_leading = pd.DataFrame()
        edge_difference = pd.DataFrame()
        normalized_data_mirror = pd.DataFrame()

        for x in leading_edge_setup:
            leading_width_label = round(x, 3)
            i = x * 1E-6
            scope = ins.scope_connection()
            func_gen = ins.func_gen_connection()
            ins.func_gen_setting_leading_edge_modify(
                func_gen, pulse_width, pulse_voltage, low, i)
            ins.func_gen_output(func_gen)
            ins.scope_setting_leading_edge(
                scope, pulse_width, pulse_voltage, low)
            data = ms.data_measure(scope)
            n_data = ms.data_slicing_leading_edge(data)
            ins.func_gen_off(func_gen)
            ins.scope_off(scope)

            n_x = n_data[0]
            n_y1 = n_data[1]
            n_y2 = n_data[2]

            EL_intensity_leading['Time (us)'] = n_x - 60
            EL_intensity_leading[f'EL intensity_{leading_width_label}us'] = n_y2
            pulse_data_leading['Time (us)'] = n_x - 60
            pulse_data_leading[f'pulse_{leading_width_label}us'] = n_y1
            normalized_data_leading['Time (us)'] = n_x - 60
            normalization= (n_y2 - min(n_y2)) / (max(n_y2) - min(n_y2))
            normalized_data_leading[f'EL normalized_{leading_width_label}us'] = normalization

            new_n_x = 100 - np.array(n_x) #for the mirroring, it depends on the horizontal scaling of scope

            normalized_data_mirror['Time (us)'] = new_n_x[::-1]
            normalized_data_mirror[f'EL normalized_{leading_width_label}us'] = normalization[::-1]
            edge_difference['Time (us)'] = new_n_x[::-1]
            EL_intensity_leading.to_csv(
                f'Leading 1. EL intensity {pulse_voltage}V {pulse_width_label}us.csv')
            pulse_data_leading.to_csv(
                f'Leading 2. pulse {pulse_voltage}V {pulse_width_label}us.csv')
            normalized_data_leading.to_csv(
                f'Leading 3. normalized data {pulse_voltage}V {pulse_width_label}us.csv')
            normalized_data_mirror.to_csv(
                f'Leading 4. normalized mirror {pulse_voltage}V {pulse_width_label}us.csv')

        for col in range(1, len(leading_edge_setup) + 1):
            edge_width = leading_edge_setup[col - 1]
            edge_difference[f'edge_differences{edge_width}'] = normalized_data_trailing.iloc[:, col] - normalized_data_mirror.iloc[:, col]
        edge_difference.to_csv(f'edge differences {pulse_voltage}V {pulse_width_label}us.csv')
        

    channel=channel_id,
    text=f'all in one, finish')
