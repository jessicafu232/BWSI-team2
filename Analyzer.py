from classes import scanAmt
import matplotlib.pyplot as plt
import numpy as np
import pickle
import math
import glob
import os

data_array = np.load("array_as_numpy.npy")

list_of_files = glob.glob('../emulator/output/*')
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)



with open(latest_file, 'rb') as f:
    positions = pickle.load(f)

c = 299792458 #m/s
t = 0.017 * scanAmt # s

print(positions)

delta_pos = positions['platform_pos'][0,0] - positions['platform_pos'][scanAmt - 1,0]
print(delta_pos)
v = abs(delta_pos / t)
wavelength = c / (4.3 * 10**9)

range_from_plane = math.sqrt((positions['platform_pos'][0,0])**2 + \
    (positions['platform_pos'][0,1])**2 + \
    (positions['platform_pos'][0,2])**2)
print(range_from_plane)

range_resolution = c / (2 * 1.1 * 10**9)
cross_range_resolution = (wavelength * range_from_plane) / (2 * delta_pos)

print(range_resolution)
print(cross_range_resolution)

np.save("array_as_numpy.npy", np.array(data_array, dtype=float), allow_pickle=True)

time = 0
times = []

full_array = np.add(np.array(data_array[0], dtype=float), np.array(data_array[1], dtype=float), np.array(data_array[2], dtype=float))

for i in range(len(full_array)):
    times += [time]
    time += int(32 * 1.907)