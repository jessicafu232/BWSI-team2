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

        # 1a) Getting the most recent platform positions file
    list_of_files = glob.glob('../emulator/output/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)

    # note: setting arbitrary values to test the next step

        # 1b) Opening file, calculations for velocity, range from midpoint of plane,
        # range rez, crange rez 
    with open(latest_file, 'rb') as f:
        positions = pickle.load(f)

    c = 299792458 #m/s

    print(positions)

    delta_pos = abs(positions['platform_pos'][0,0] - positions['platform_pos'][scanAmt - 1, 0])
    wavelength = c / (4.3 * 10**9)
    range_from_plane = math.sqrt((positions['platform_pos'][0,0])**2 + (positions['platform_pos'][0,1])**2 + \
        (positions['platform_pos'][0,2])**2)

    range_resolution = c / (2 * 1.1 * 10**9)
    cross_range_resolution = (wavelength * range_from_plane) / (2 * delta_pos)

    print('range', range_resolution)
    print('cross range', cross_range_resolution)

    #np.save("array_as_numpy.npy", np.array(data_array, dtype=float), allow_pickle=True)
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

    

    print(len(data_array[0]))

    '''
    for i in range(Y_RES):
        for j in range(X_RES):
            # position in meters
            x_position_of_pixel = j * pixel_x
            y_position_of_pixel = i * pixel_y

            distance_to_scan = math.sqrt(
                (positions['platform_pos'][0,0] - x_position_of_pixel + 10)**2 + \
                (positions['platform_pos'][0,1] - y_position_of_pixel + 10)**2 + \
                (positions['platform_pos'][0,2])**2 \
                )

            #print(distance_to_scan)
            ind = range_to_index(distance_to_scan)
            if ind > 4127: continue
            #print('index', ind)
            amplitude = data_array[(scan, ind)]
            #print('amplitude', amplitude)
            potentials[j,i] += amplitude
    '''
    import time
    start_time = time.time()

    for scan in range(3):
        break
        for i in range(Y_RES):
            for j in range(X_RES):  
                # position in meters
                x_position_of_pixel = j * pixel_x
                y_position_of_pixel = i * pixel_y
                which_scan = scan * 10

                distance_to_scan = math.sqrt(
                    (positions['platform_pos'][which_scan,0] - x_position_of_pixel + 10)**2 + \
                    (positions['platform_pos'][which_scan,1] - y_position_of_pixel + 10)**2 + \
                    (positions['platform_pos'][which_scan,2])**2 \
                )
    
                #print(distance_to_scan)
                ind = range_to_index(distance_to_scan)
                if ind > 4127: continue
                #print('index', ind)
                amplitude = data_array[(which_scan, ind)]
                #print('amplitude', amplitude)
                potentials[i,j] += amplitude
    # dimensions of the original image (m)
    X = 20
    Y = 20
    X_RES, Y_RES = 200, 200
    potentials = np.zeros((X_RES, Y_RES))
    # finding dimensions of a single pixel
    pixel_x = X / X_RES
    pixel_y = Y / Y_RES

    for scan in range(scanAmt):
        which_scan = scan
        x_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES) * X / X_RES
        y_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES).T * Y / Y_RES
        distance_to_scan = np.sqrt(
                            (positions['platform_pos'][which_scan,0] - x_pos + 10)**2 + \
                            (positions['platform_pos'][which_scan,1] - y_pos + 10)**2 + \
                            (positions['platform_pos'][which_scan,2])**2 
                            )
        times = 2 * distance_to_scan / 299792458 
        indexes = np.rint(times / 61.024e-12)
        indexes = np.minimum(indexes, data_array.shape[1] - 1)
        for i in range(Y_RES):
            for j in range(X_RES):
                potentials[i,j] += data_array[which_scan, int(indexes[i,j])]
    print('max potential', np.max(potentials), '\nminpotential', np.min(potentials))
        #print('time', time.time()-start_time)
    '''
    for scan in range(24):
        for i in range(Y_RES):
            for j in range(X_RES):
                distance_to_scan = math.sqrt((positions['platform_pos'][scan*20,0] - i/40) **2 + (positions['platform_pos'][scan*20,1] - j/40)**2 + \
                    (positions['platform_pos'][scan*20,2])**2)
                #print(f'{i}, {j}, distance',distance_to_scan)
                index = range_to_index(distance_to_scan) - 2786
                #print(i)
                if abs(index) > 699: continue
                amplitude = data_array[scan*20, index]
                potentials[i,j] += amplitude
    '''

    plt.imshow(potentials)
    plt.show()

# I love basic radar eq
from basic_radar_equation import basic_radar_eq_mk2

def range_to_index(rng):
    time = basic_radar_eq_mk2(rng)
    index = round(time / 61.024e-12)
    #print('index',index)
    return index

if __name__ == '__main__':
    main()