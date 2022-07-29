import numpy as np
which_scan = np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][0].astype(np.uint16)
print('finished creating which scan with shape',which_scan.shape)
'''
x_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES) * X / X_RES
y_pos = np.mod(np.arange(X_RES*Y_RES).reshape(X_RES, Y_RES), X_RES).T * Y / Y_RES
'''
x_pos, y_pos = np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][1:].astype(np.uint16)
x_pos = x_pos 
y_pos = y_pos 
platform_pos = platform_pos.astype(np.float16)
print('finished creating x_pos and y_pos')
# np.linalg.tensordot()
distance_to_scan = np.sqrt(
                    (platform_pos[which_scan,0] - x_pos * X / X_RES + x_offset)**2 + \
                    (platform_pos[which_scan,1] - y_pos * Y / Y_RES + y_offset)**2 + \
                    (platform_pos[which_scan,2])**2 
                    
                    )
# a dot b = a^2 + b^2
del x_pos, y_pos
print('finished calculating distances')
times = 2 * distance_to_scan / 299792458 
del distance_to_scan
indexes = np.rint(times / 61.024e-12)
del times
indexes = np.minimum(indexes, data_array.shape[1] - 1)
print('finished calculating indexes')
potentials = data_array[which_scan, indexes.astype(int)]
print('finished calculating potentials')
potentials = np.sum(potentials, 0)
minimum = np.min(potentials)
if config.get('Contrast') is None: contrast = 1
potentials = potentials + abs(minimum)
potentials = potentials ** contrast
print(potentials)

image = data_array[np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][0].astype(np.uint16), np.minimum(
            np.rint(
                2 *
                np.sqrt( \
                    (platform_pos[np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][0].astype(np.uint16),0] - np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][1:].astype(np.uint16)[0] * X / X_RES + x_offset)**2 + \
                    (platform_pos[np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][0].astype(np.uint16),1] - np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][1:].astype(np.uint16)[1] * Y / Y_RES + y_offset)**2 + \
                    (platform_pos[np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][0].astype(np.uint16),2])**2 \
                ) 
            / 299792458 / 61.024e-12
            )
            data_array.shape[1] - 1)]

image = data_array[np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][0].astype(np.uint16), np.minimum(np.rint(2 * np.sqrt((platform_pos[np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][0].astype(np.uint16),0] - np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][1:].astype(np.uint16)[0] * X / X_RES + x_offset)**2 + (platform_pos[np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][0].astype(np.uint16),1] - np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][1:].astype(np.uint16)[1] * Y / Y_RES + y_offset)**2 + (platform_pos[np.mgrid[0:scanAmt, 0:Y_RES, 0:X_RES][0].astype(np.uint16),2])**2 ) / 299792458 / 61.024e-12), data_array.shape[1] - 1)]