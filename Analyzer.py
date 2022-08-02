import matplotlib.pyplot as plt
import numpy as np
import pickle
import json
import math
import glob
import os
import argparse
from tqdm import tqdm
import pandas
import time

DEFAULT_CONFIG = './five_point_config.json'
DEFAULT_DATA = 'array_as_numpy.npy'

parser = argparse.ArgumentParser(description="Analyse data")
parser.add_argument("--datafile", '-df', default=DEFAULT_DATA,help='Location of datafile')
parser.add_argument("--config", '-c', default=DEFAULT_CONFIG, help='Location of a configuration file')
parser.add_argument("--mode", '-em', default='true', help='Run a file through emulator, true or false')
args = parser.parse_args()

colormap = 'magma'
non_emulator_file = 'marathon_0.pkl'
def main():

    list_of_files = glob.glob('../emulator/output/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(args.config, 'r') as f:
        config = json.load(f)
    print(config)
    
    if args.mode == 'true':
        print("Running emulator data!!!")
        data_array = np.load(args.datafile)
        with open(latest_file, 'rb') as f:
            positions = pickle.load(f)
        platform_pos = positions['platform_pos']
        scanAmt= config['Scan Amount']
    else:
        print("Running non-emulator data!!!")
        x = pandas.read_pickle(non_emulator_file)
        print(x)
        data_array = x['scan_data']
        platform_pos = x['platform_pos']
        print(data_array.shape, platform_pos.shape)
        scanAmt = data_array.shape[0] 
        range_bins = x['range_bins']


    # note: setting arbitrary values to test the next step

        # 1b) Opening file, calculations for velocity, range from midpoint of plane,
        # range rez, crange rez 

    contrast = config['Contrast']
    c = 299792458 #m/s

    delta_pos = abs(platform_pos[0,0] - platform_pos[scanAmt - 1, 0])
    wavelength = c / (4.3 * 10**9)
    range_from_plane = math.sqrt((platform_pos[0,0])**2 + (platform_pos[0,1])**2 + \
        (platform_pos[0,2])**2)

    range_resolution = c / (2 * 1.1 * 10**9)
    cross_range_resolution = (wavelength * range_from_plane) / (2 * delta_pos)

    print('range', range_resolution)
    print('cross range', cross_range_resolution)

    #np.save("array_as_numpy.npy", np.array(data_array, dtype=float), allow_pickle=True)
    # Will find out later what this is

    # 2) Using our Pixel Size, finding distance from each pixel to the platform, then using
    # this we calculate the time of the signal to send and come back. Then, knowing the delay 
    # between each individual scanpoint, we align that time to the scan data time, and then
    # assign that amplitude value to that pixel.     

    start_time = time.time()

    # dimensions of the original image (m)
    X = config['X']
    Y = config['Y']
    X_RES, Y_RES = config['X_RES'], config['Y_RES']
    potentials = np.zeros((X_RES, Y_RES)).astype(data_array.dtype)

    # finding dimensions of a single pixel
    pixel_x = X / X_RES
    pixel_y = Y / Y_RES

    # labels
    ticks_x = []
    ticks_y = []
    # locations of ticks relative to pixels
    tick_dimensions = np.arange(0, X_RES, X_RES / 10)

    # offset = the amount the image is offset
    x_offset = config['X_OFFSET']
    y_offset = config['Y_OFFSET']

    # looping through and creating a list with each tick value, for ten total ticks.
    # the tick amount is the same for every image, but the size between ticks differs
    for tick in range(10):
        ticks_x.append(round(tick * (X / 10) - x_offset, 1))
        ticks_y.append(round(tick * (Y / 10) - y_offset, 1))

    tdct = 0
    
    x_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES) * X / X_RES
    y_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES).T * Y / Y_RES

    print(x_pos.dtype)

    time_loop = 0

    timetime = 0 
    indextime = 0

    start_time_loop = time.time()

    z = platform_pos[0, 2]


    '''
    @cache
    def wrapper(x):
        return np.sqrt(x)
    '''

    for scan in tqdm(range(scanAmt)):
        which_scan = scan
        dcst = time.time() # distance calculation start time

        x = platform_pos[which_scan, 0] + x_offset
        y = platform_pos[which_scan, 1] + y_offset
        
        distance_to_scan = np.sqrt(
                            (x - x_pos)**2 + \
                            (y - y_pos)**2 + \
                            (z)**2 
                            )
        tdct += time.time() - dcst # total distance calculation time

        if args.mode == 'true':
            ttst = time.time()
            times = 2 * distance_to_scan / c 
            timetime += time.time() - ttst

            itst = time.time()
            indexes = times / (61.024e-12)
            indextime += time.time() - itst
        else:
            start_time_no_emulator = 2 * np.min(range_bins) / c
            end_scan = 2 * np.max(range_bins) / c
            #print("start scan", start_time_no_emulator * 10**12, "end scan", end_scan * 10**12)
            times = (2 * distance_to_scan / c) - start_time_no_emulator
            diff = (end_scan - start_time_no_emulator) / len(range_bins)
            indexes = times / diff
            
            '''
            # matching the distance_to_scan values with the range_bins value
            index_sorted = np.argsort(range_bins)
            range_bins_sorted = range_bins[index_sorted]
            idx1 = np.searchsorted(range_bins_sorted, distance_to_scan)
            idx2 = np.clip(idx1 - 1, 0, len(range_bins_sorted) - 1)

            diff1 = range_bins_sorted[idx1] - distance_to_scan
            diff2 = distance_to_scan - range_bins_sorted[idx2]

            # indexes of the closest range_bins value to each pixel.
            # using this index we can figure out which amplitude is the best for every pixel
            # b/c its distance is the most similar
            indexes = index_sorted[np.where(diff1 <= diff2, idx1, idx2)]
            residual = distance_to_scan - range_bins[indexes]
            # print(residual)
            '''
            '''
            for i in range(Y_RES):
                for j in range(X_RES):
                    ci = np.argmin(np.abs(range_bins - distance_to_scan[i,j]))
                    potentials[i,j] += data_array[which_scan, ci]
            '''
            
        
        indexes = np.minimum(indexes.astype(int), data_array.shape[1] - 1)
        potentials += data_array[which_scan, indexes]

    time_loop = time.time() - start_time_loop

    minimum = np.min(potentials)
    if config.get('Contrast') is None: contrast = 1

    # checking if there are complex numbers, if so then skipping the contrast, if not then running contrast 
    if not np.iscomplexobj(potentials):
        potentials = potentials + abs(minimum)
        potentials = potentials ** contrast
    print(potentials)
    potentials = np.abs(potentials)

    print("time calc time", timetime, timetime/(time.time()-start_time) * 100, '%')
    print("indextime", indextime, indextime/(time.time()-start_time) * 100, '%')


    print('max potential', np.max(potentials), '\nminpotential', np.min(potentials))
    print('total time', time.time()-start_time)
    print('time spent calculating distances', tdct, 'sec - ', tdct/(time.time()-start_time) * 100, '%')
    plt.xlabel("Crossrange (m)")
    plt.ylabel("Range (m)")

    plt.xticks(tick_dimensions, ticks_x)
    plt.yticks(tick_dimensions, ticks_y)

    plt.imshow(potentials, origin='lower', cmap=colormap)
    plt.colorbar()
    plt.show()

if __name__ == '__main__':
    main()
