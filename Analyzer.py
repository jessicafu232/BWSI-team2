from classes import scanAmt
import matplotlib.pyplot as plt
import numpy as np
import pickle
import math
import glob
import os


def main():
    # 1) finding the range and cross range resolutions
    data_array = np.load('array_as_numpy.npy')

    scanAmt = 5
        # 1a) Getting the most recent platform positions file
    list_of_files = glob.glob('../emulator/output/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)

    # note: setting arbitrary values to test the next step
    X_RES, Y_RES = 100, 100
    potentials = np.zeros((X_RES, Y_RES))

        # 1b) Opening file, calculations for velocity, range from midpoint of plane,
        # range rez, crange rez 
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
# Will find out later what this is
    time = 0
    times = []

    full_array = np.add(np.array(data_array[0], dtype=float), np.array(data_array[1], dtype=float), np.array(data_array[2], dtype=float))

    for i in range(len(full_array)):
        times += [time]
        time += int(32 * 1.907)

    # 2) Using our Pixel Size, finding distance from each pixel to the platform, then using
    # this we calculate the time of the signal to send and come back. Then, knowing the delay 
    # between each individual scanpoint, we align that time to the scan data time, and then
    # assign that amplitude value to that pixel. 
    for i in range(Y_RES):
        for j in range(X_RES):
            distance_to_scan = math.sqrt((positions['platform_pos'][0,0] - (i/X_RES*4)) **2 + (positions['platform_pos'][0,1] - (j/Y_RES*4))**2 + \
                (positions['platform_pos'][0,2])**2)
            #print(f'{i}, {j}, distance',distance_to_scan)
            index = range_to_index(distance_to_scan)-2786
            #print(i)
            if index > 699: continue
            amplitude = data_array[0, index]
            potentials[i,j] += amplitude

    plt.imshow(potentials)
    plt.show()
# I love basic radar eq
from basic_radar_equation import basic_radar_eq_mk2

def range_to_index(range):
    time = basic_radar_eq_mk2(range)
    index = round(time / 61.024e-12)
    return index - 1

if __name__ == '__main__':
    main()