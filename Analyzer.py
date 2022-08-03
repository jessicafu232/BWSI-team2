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
from pyfiglet import Figlet

DEFAULT_CONFIG = './five_point_config.json'
DEFAULT_DATA = 'array_as_numpy.npy'

# name of file to save (change every image)
fileName = "image1_img.pkl"

# adding parser arguments
parser = argparse.ArgumentParser(description="Analyse data")
parser.add_argument("--datafile", '-df', default=DEFAULT_DATA,help='Location of datafile')
parser.add_argument("--config", '-c', default=DEFAULT_CONFIG, help='Location of a configuration file')
parser.add_argument("--mode", '-em', default='true', help='Run a file through emulator, true or false')
parser.add_argument("--fname", '-fn', default=fileName, help='Name of the final dictionary to save' )
args = parser.parse_args()

colormap = 'magma'
non_emulator_file = 'marathon_0.pkl'

def main():

    f = Figlet(font='slant')
    b = Figlet(font='mini')

    print(f.renderText('OLIVES'), b.renderText("by team 2"))

    list_of_files = glob.glob('../emulator/output/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(args.config, 'r') as f:
        config = json.load(f)
    print("YOUR CONFIGURATION:", config)
    print("\nCURRENTLY:")
    
    if args.mode == 'true':
        print("Running emulator data!!!\n")
        data_array = np.load(args.datafile)
        with open(latest_file, 'rb') as f:
            positions = pickle.load(f)
        platform_pos = positions['platform_pos']
        scanAmt= config['Scan Amount']
    else:
        print("Running non-emulator data!!!\n")
        x = pandas.read_pickle(non_emulator_file)
        data_array = x['scan_data']
        platform_pos = x['platform_pos']
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

    # skip amout
    skip = config['Skip']

    # looping through and creating a list with each tick value, for ten total ticks.
    # the tick amount is the same for every image, but the size between ticks differs
    for tick in range(10):
        ticks_x.append(round(tick * (X / 10) - x_offset, 1))
        ticks_y.append(round(tick * (Y / 10) - y_offset, 1))
    
    x_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES) * X / X_RES
    y_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES).T * Y / Y_RES

    tdct = 0
    time_loop = 0
    timetime = 0 
    indextime = 0

    start_time_loop = time.time()

    z = platform_pos[0, 2]

    print("\nRendering image...")

    for scan in tqdm(range(scanAmt // skip)):
        which_scan = scan * skip
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
            # calculating the start time of the scan data without running through emulator
            # necessary in order to index using time
            start_time_no_emulator = 2 * np.min(range_bins) / c
            end_time_no_emulator = 2 * np.max(range_bins) / c

            times = (2 * end_time_no_emulator / c) - start_time_no_emulator
            diff = (distance_to_scan - start_time_no_emulator) / len(range_bins)
            indexes = times / diff
            indexes = indexes
        
        # making sure the indexes aren't out of bounds of the array
        indexes = np.minimum(indexes.astype(int), data_array.shape[1] - 1)

        # inputting the amplitudes into its correct position in the final (potentials) array
        potentials += data_array[which_scan, indexes]


    # time of the entire for loop
    time_loop = time.time() - start_time_loop

    # saving the unprocessed image data into the final dictionary
    finalDict = {
        'img': potentials,
        'x': x_pos,
        'y': y_pos
    }

    # save file
    f = open(args.fname, 'wb')
    pickle.dump(finalDict, f)
    f.close()

    # setting variables to run contrast processing
    minimum = np.min(potentials)
    if config.get('Contrast') is None: contrast = 1

    # checking if there are complex numbers, if so then skipping the contrast, if not then running contrast 
    if not np.iscomplexobj(potentials):
        potentials = potentials + abs(minimum)
        potentials = potentials ** contrast
    potentials = np.abs(potentials)

    print('Max potential', np.max(potentials), '\nminpotential', np.min(potentials))
    print("Time spent to calculate the time", timetime, "seconds, or", timetime/(time.time()-start_time) * 100, '%')
    print("Time spent to index the array", indextime, "seconds, or", indextime/(time.time()-start_time) * 100, '%')
    print('Time spent calculating distances', tdct, 'seconds, or', tdct/(time.time()-start_time) * 100, '%')
    print('Total time', time.time()-start_time)


    # plotting the image in matplotlib
    plt.xlabel("Crossrange (m)")
    plt.ylabel("Range (m)")

    plt.xticks(tick_dimensions, ticks_x)
    plt.yticks(tick_dimensions, ticks_y)

    plt.imshow(potentials, origin='lower', cmap=colormap)
    plt.colorbar()
    plt.show()

if __name__ == '__main__':
    main()
