from classes import scanAmt
import matplotlib.pyplot as plt
import numpy as np
import pickle
import math
import glob
import os


def main():
    data_array = np.load('array_as_numpy.npy')

    list_of_files = glob.glob('../emulator/output/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)

    X_RES, Y_RES = 800, 800
    potentials = np.zeros((X_RES, Y_RES))

    with open(latest_file, 'rb') as f:
        positions = pickle.load(f)

    c = 299792458 #m/s
    t = 0.017 * scanAmt # s

    print(positions)

    delta_pos = positions['platform_pos'][0,0] - positions['platform_pos'][scanAmt - 1, 0]
    v = abs(delta_pos / t)
    wavelength = c / (4.3 * 10**9)
    range_from_plane = math.sqrt((positions['platform_pos'][0,0])**2 + (positions['platform_pos'][0,1])**2 + \
        (positions['platform_pos'][0,2])**2)

    range_resolution = c / (2 * 1.1 * 10**9)
    cross_range_resolution = (wavelength * range_from_plane) / (2 * v * t)

    print('range', range_resolution)
    print('cross range', cross_range_resolution)

    np.save("array_as_numpy.npy", np.array(data_array, dtype=float), allow_pickle=True)

    time = 0
    times = []

    full_array = np.add(np.array(data_array[0], dtype=float), np.array(data_array[1], dtype=float), np.array(data_array[2], dtype=float))

    for i in range(len(full_array)):
        times += [time]
        time += int(32 * 1.907)

    for scan in range(9):
        for i in range(Y_RES):
            for j in range(X_RES):
                distance_to_scan = math.sqrt((positions['platform_pos'][scan*50,0] - (i/X_RES*-50)) **2 + (positions['platform_pos'][scan*50,1] - (j/Y_RES*50))**2 + \
                    (positions['platform_pos'][scan*50,2])**2)
                #print(f'{i}, {j}, distance',distance_to_scan)
                index = range_to_index(distance_to_scan) - 3500
                #print(i)
                if abs(index) > 699: continue
                amplitude = data_array[scan*50, index]
                potentials[i,j] += amplitude

    plt.imshow(potentials)
    plt.show()

from basic_radar_equation import basic_radar_eq_mk2

def range_to_index(range):
    time = basic_radar_eq_mk2(range)
    index = round(time / 61.024e-12)
    return index - 1

if __name__ == '__main__':
    main()