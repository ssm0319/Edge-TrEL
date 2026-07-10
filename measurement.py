import os
import instrument as ins
import time
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import numpy as np

ref_path = r'F:\OneDrive\Transient EL\data\\'

def saving_folder(ref_path, folder_name):
    os.chdir(ref_path)
    try:
        os.mkdir(folder_name)
        os.chdir(ref_path + folder_name)
    except:
        os.chdir(ref_path + folder_name)
    return ref_path+folder_name + '\\'

def data_measure(scope):
    time.sleep(1) #waiting for stabilization
    data1 = ins.scope_ascii_measure(scope)
    time.sleep(0.001)
    data2 = ins.scope_ascii_measure(scope)
    time.sleep(0.001)
    data3 = ins.scope_ascii_measure(scope)
    x = (data1[0] + data2[0] + data3[0]) / 3
    # EL intensity: y1 (y1 need inverse)
    y1 = (data1[1] + data2[1] + data3[1]) / 3
    y2 = (data1[2] + data2[2] + data3[2]) / 3
    xinc = x[1] - x[0]
    data = [x, y1, y2, xinc]
  
    return data

def data_slicing(data):
    xinc = data[3]
    pulse_period_index = int(len(data[0]) / 2)
    x = data[0] - xinc * pulse_period_index
    n_x = x[pulse_period_index - 2000:]
    n_y1 = data[1][pulse_period_index - 2000:]
    n_y2 = data[2][pulse_period_index - 2000:]
    smooth_1 = savgol_filter(n_y2, 30, 2)
    n_x_final = np.round(n_x, decimals=6).astype('float32')
    n_y1_final = np.round(n_y1, decimals=6).astype('float32')
    n_y2_final = np.round(n_y2, decimals=6).astype('float32')  
    smooth_1_final = np.round(smooth_1, decimals=6).astype('float32')  
    return n_x_final, n_y1_final, n_y2_final, smooth_1_final

def data_slicing_leading_edge(data):
    xinc = data[3]
    pulse_period_index = int(len(data[0]) / 2)
    x = data[0]
    n_x = x[:pulse_period_index+2000]
    n_y1 = data[1][:pulse_period_index+2000]
    n_y2 = data[2][:pulse_period_index+2000]
    smooth_1 = savgol_filter(n_y2, 30, 2)

    return n_x, n_y1, n_y2, smooth_1
