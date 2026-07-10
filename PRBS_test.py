import VLC_module

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

import time

ref_path_bandwidth = r'F:\OneDrive\Transient EL\bandwidth\\'

bit_arr = np.arange(1,3.1,0.1)

for i in bit_arr:
    bit_rate =i*1e6 #1Mbps
    voltage = 5
    low = 0
    folder_name = f'file_name, {voltage} V'
    print (bit_rate)
    os.chdir(ref_path_bandwidth)
    try:
        os.mkdir(folder_name)
        os.chdir(ref_path_bandwidth + folder_name)
    except:
        os.chdir(ref_path_bandwidth + folder_name)


    func_gen = VLC_module.func_gen_connection()
    scope = VLC_module.scope_connection()
    frequency = bit_rate/127

    VLC_module.funcgen_prbs_setting(func_gen, bit_rate, voltage, low)
    VLC_module.scope_setting(scope, bit_rate,voltage, low)
    VLC_module.func_gen_output(func_gen)

    time.sleep(1)
    PRBS_data = pd.DataFrame()
    for i in range (0,10):
        data = VLC_module.scope_ascii_measure(scope)
        x = data[0]
        y2 = data[2]
        PRBS_data['Time'] = x
        PRBS_data[f'PRBS_{i}'] = y2

        plt.plot(PRBS_data['Time'], PRBS_data[f'PRBS_{i}'])


    plt.savefig(f"PRBS_{bit_rate/1E6}Mbps, {voltage}V.png", dpi=660)
    PRBS_data.to_csv(f"PRBS_{bit_rate/1E6}Mbps, {voltage}V.csv")

    VLC_module.func_gen_off(func_gen)
    VLC_module.scope_off(scope)





