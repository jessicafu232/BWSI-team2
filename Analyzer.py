import matplotlib.pyplot as plt
#import matplotlib as mpl
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
parser.add_argument("--mode", '-em', default='yes', help='Run a file through emulator, true or false')
args = parser.parse_args()

def main():
    x= pandas.read_pickle(r'marathon_0.pkl')
    print(x) 

    data_array = x['scan_data']
    platform_pos = x['platform_pos']
    range_bins = x['range_bins']

    
    #data_array = np.load(args.datafile)
    print(args)
    with open(args.config, 'r') as f:
        config = json.load(f)
    print(config)
        # 1a) Getting the most recent platform positions file
    list_of_files = glob.glob('../emulator/output/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)

    # note: setting arbitrary values to test the next step

        # 1b) Opening file, calculations for velocity, range from midpoint of plane,
        # range rez, crange rez 
    with open(latest_file, 'rb') as f:
        positions = pickle.load(f)

    print(positions)

    c = 299792458 #m/s

    delta_pos = abs(platform_pos[0,0] - platform_pos[config['Scan Amount'] - 1, 0])
    wavelength = c / (4.3 * 10**9)
    range_from_plane = math.sqrt((platform_pos[0,0])**2 + (platform_pos[0,1])**2 + \
        (platform_pos[0,2])**2)
    
    #if using the emulator, use this instead
    '''
    delta_pos = abs(positions['platform_pos'][0,0] - positions['platform_pos'][config['Scan Amount'] - 1, 0])
    wavelength = c / (4.3 * 10**9)
    range_from_plane = math.sqrt((positions['platform_pos'][0,0])**2 + (positions['platform_pos'][0,1])**2 + \
        (positions['platform_pos'][0,2])**2)'''

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
    potentials = np.zeros((X_RES, Y_RES))
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

    for scan in tqdm(range(len(data_array) // config['Skip'])):
        which_scan = scan * config['Skip']
        x_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES) * X / X_RES
        y_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES).T * Y / Y_RES
        distance_to_scan = np.sqrt(
                            (platform_pos[which_scan,0] - x_pos + x_offset)**2 + \
                            (platform_pos[which_scan,1] - y_pos + y_offset)**2 + \
                            (platform_pos[which_scan,2])**2 
                            )
        times = 2 * distance_to_scan / 299792458 
        indexes = np.rint(times / 61.024e-12)
        indexes = np.minimum(indexes, data_array.shape[1] - 1)
        potentials += np.abs(data_array[which_scan, indexes.astype(int)])

    minimum = np.min(potentials)

    potentials = potentials + abs(minimum)
    potentials = potentials ** 3
    print(potentials)


    print('max potential', np.max(potentials), '\nminpotential', np.min(potentials))
    print('time', time.time()-start_time)
    
    plt.xlabel("Crossrange (m)")
    plt.ylabel("Range (m)")

    plt.xticks(tick_dimensions, ticks_x)
    plt.yticks(tick_dimensions, ticks_y)

    plt.imshow(potentials, origin='lower', cmap='bone')
    plt.show()

def main2():
    # 1) finding the range and cross range resolutions
    parser = argparse.ArgumentParser(description="Analyse data")
    parser.add_argument("--datafile", '-df', default=DEFAULT_DATA,help='Location of datafile')
    parser.add_argument("--config", '-c', default=DEFAULT_CONFIG, help='Location of a configuration file')
    args = parser.parse_args()
    data_array = np.load(args.datafile)
    print(args)
    with open(args.config, 'r') as f:
        config = json.load(f)
    print(config)
        # 1a) Getting the most recent platform positions file
    list_of_files = glob.glob('../emulator/output/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)

    # note: setting arbitrary values to test the next step

        # 1b) Opening file, calculations for velocity, range from midpoint of plane,
        # range rez, crange rez 
    with open(latest_file, 'rb') as f:
        positions = pickle.load(f)

    print(positions)

    c = 299792458 #m/s

    delta_pos = abs(positions['platform_pos'][0,0] - positions['platform_pos'][config['Scan Amount'] - 1, 0])
    wavelength = c / (4.3 * 10**9)
    range_from_plane = math.sqrt((positions['platform_pos'][0,0])**2 + (positions['platform_pos'][0,1])**2 + \
        (positions['platform_pos'][0,2])**2)

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
    potentials = np.zeros((X_RES, Y_RES))
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

    for scan in tqdm(range(config['Scan Amount'] // config['Skip'])):
        which_scan = scan * config['Skip']
        x_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES) * X / X_RES
        y_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES).T * Y / Y_RES
        distance_to_scan = np.sqrt(
                            (positions['platform_pos'][which_scan,0] - x_pos + x_offset)**2 + \
                            (positions['platform_pos'][which_scan,1] - y_pos + y_offset)**2 + \
                            (positions['platform_pos'][which_scan,2])**2 
                            )
        times = 2 * distance_to_scan / 299792458 
        indexes = np.rint(times / 61.024e-12)
        indexes = np.minimum(indexes, data_array.shape[1] - 1)
        potentials += np.abs(data_array[which_scan, indexes.astype(int)])
    minimum = np.min(potentials)

    potentials = potentials + abs(minimum)
    potentials = potentials ** 3
    print(potentials)


    print('max potential', np.max(potentials), '\nminpotential', np.min(potentials))
    print('time', time.time()-start_time)
    
    plt.xlabel("Crossrange (m)")
    plt.ylabel("Range (m)")

    plt.xticks(tick_dimensions, ticks_x)
    plt.yticks(tick_dimensions, ticks_y)

    plt.imshow(potentials, origin='lower', cmap='bone')
    plt.show()

# I love basic radar eq
from basic_radar_equation import basic_radar_eq_mk2

def range_to_index(rng):
    time = basic_radar_eq_mk2(rng)
    index = round(time / 61.024e-12)
    #print('index',index)
    return index

if args.mode == 'yes':
    main2()
else:
    main()
