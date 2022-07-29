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

DEFAULT_CONFIG = './marathon_0_config.json'
DEFAULT_DATA = 'array_as_numpy.npy'

parser = argparse.ArgumentParser(description="Analyse data")
parser.add_argument("--datafile", '-df', default=DEFAULT_DATA,help='Location of datafile')
parser.add_argument("--config", '-c', default=DEFAULT_CONFIG, help='Location of a configuration file')
parser.add_argument("--mode", '-em', default='true', help='Run a file through emulator, true or false')
args = parser.parse_args()


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
        x = pandas.read_pickle(r'marathon_0.pkl')
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

    import time
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

    for scan in tqdm(range(scanAmt // config['Skip'])):
        which_scan = scan * config['Skip']
        x_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES) * X / X_RES
        y_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES).T * Y / Y_RES
        distance_to_scan = np.sqrt(
                            (platform_pos[which_scan,0] - x_pos + x_offset)**2 + \
                            (platform_pos[which_scan,1] - y_pos + y_offset)**2 + \
                            (platform_pos[which_scan,2])**2 
                            )

        if args.mode == 'true':
            times = 2 * distance_to_scan / 299792458 
            indexes = np.rint(times / 61.024e-12)
        else:
            start_time_no_emulator = 2 * np.min(range_bins) / 299792458
            end_scan = 2 * np.max(range_bins) / 299792458
            #print("start scan", start_time_no_emulator * 10**12, "end scan", end_scan * 10**12)
            times = (2 * distance_to_scan / 299792458) - start_time_no_emulator
            #print("last one calc", times[0][-1] * 10**12, "last one hypo", (end_scan - start_time_no_emulator) * 10**12)
            #print("diff", ((end_scan - start_time_no_emulator) * 10**12) / len(range_bins))
            diff = (end_scan - start_time_no_emulator) / len(range_bins)
            indexes = np.rint(times / diff)
            
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
            
        
        indexes = np.minimum(indexes, data_array.shape[1] - 1)
        potentials += data_array[which_scan, indexes.astype(int)]
    minimum = np.min(potentials)
    if config.get('Contrast') is None: contrast = 1

    # checking if there are complex numbers, if so then skipping the contrast, if not then running contrast 
    if not np.iscomplexobj(potentials):
        potentials = potentials + abs(minimum)
        potentials = potentials ** contrast
    print(potentials)
    potentials = np.abs(potentials)


    print('max potential', np.max(potentials), '\nminpotential', np.min(potentials))
    print('time', time.time()-start_time)
    
    plt.xlabel("Crossrange (m)")
    plt.ylabel("Range (m)")

    plt.xticks(tick_dimensions, ticks_x)
    plt.yticks(tick_dimensions, ticks_y)

    plt.imshow(potentials, origin='lower', cmap='copper')
    plt.colorbar()
    plt.show()

main()
