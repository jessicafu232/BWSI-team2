from classes import Encoder, Decoder, PORT, SIZES, data_array, scanAmt
import socket, struct
import matplotlib.pyplot as plt
import numpy as np
import pickle
import math
import glob
import os

scan_start = 0
scan_end = 250000

ENCODER = Encoder(['Settings Header', 'UINT16', 0xfffe],
                ['Message ID',  'UINT16',    30],
                ['uint8',       'UINT8',     69],
                ['uint16',      'UINT16',    420],
                ['uint32',      'UINT32',    69420],
                ['int8',        'INT8',      -69],
                ['int16',       'INT16',     -420],
                ['int32',       'INT32',     -69420]) 

DECODER = Decoder(
    ['Settings Header', 'UINT16' ]  ,
    ['Message ID', 'UINT16' ]       ,
    ['UINT8'     , 'UINT8'    ]     ,
    ['UINT16'    , 'UINT16'   ]     ,
    ['UINT32'    , 'UINT32'   ]     ,
    ['INT8'      , 'INT8'     ]     ,
    ['INT16'     , 'INT16'    ]     ,
    ['INT32'     , 'INT32'    ]     ,
    ['CHAR[15]'  , 'CHAR[15]' ]     ,
    ['Status'    , 'UINT32' ]
)

ENCODER31 = Encoder(['Settings Header', 'UINT16', 0x1001],
                ['Message ID', 'UINT16', 31],
                ['Node ID', 'UINT32', 1],
                ['Scan Start (ps)', 'INT32', scan_start],
                ['Scan End (ps)', 'INT32', scan_end],
                ['Scan Resolution (bins)', 'UINT16', 32],
                ['Base Integration Index', 'UINT16', 11],
                ['Segment 1 Num Samples', 'UINT16', 13],
                ['Segment 2 Num Samples', 'UINT16', 15],
                ['Segment 3 Num Samples', 'UINT16', 17],
                ['Segment 4 Num Samples', 'UINT16', 19],
                ['Segment 1 Integration Multiple', 'UINT8', 1],
                ['Segment 2 Integration Multiple', 'UINT8', 2],
                ['Segment 3 Integration Multiple', 'UINT8', 3],
                ['Segment 4 Integration Multiple', 'UINT8', 4],
                ['Antenna Mode', 'UINT8', 2],
                ['Transmit Gain', 'UINT8', 63],
                ['Code Channel', 'UINT8', 0],
                ['Persist Flag', 'UINT8', 0])

DECODER32 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )

ENCODER33 = Encoder(['Settings Header', 'UINT16', 0x1002],
                    ['Message ID', 'UINT16', 33])

DECODER34 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Node ID', 'UINT32'],
                ['Scan Start (ps)', 'INT32'],
                ['Scan End (ps)', 'INT32'],
                ['Scan Resolution', 'UINT16'],
                ['Base Integration Index', 'UINT16'],
                ['Segment 1 Num Samples', 'UINT16'],
                ['Segment 2 Num Samples', 'UINT16'],
                ['Segment 3 Num Samples', 'UINT16'],
                ['Segment 4 Num Samples', 'UINT16'],
                ['Segment 1 Integration Multiple', 'UINT8'],
                ['Segment 2 Integration Multiple', 'UINT8'],
                ['Segment 3 Integration Multiple', 'UINT8'],
                ['Segment 4 Integration Multiple', 'UINT8'],
                ['Antenna Mode', 'UINT8'],
                ['Transmit Gain', 'UINT8'],
                ['Code Channel', 'UINT8'],
                ['Persist Flag', 'UINT8'],
                ['Timestamp', 'UINT32'],
                ['Status', 'UINT32'])

ENCODER35 = Encoder(['Settings Header', 'UINT16', 0x1003],
                ['Message ID', 'UINT16', 35],
                ['Scan Count', 'UINT16', scanAmt],
                ['Reserved', 'UINT16', 3],
                ['Scan Interval Time', 'UINT32', 5]
                )

DECODER36 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )

DECODER21 = Decoder(['Settings Header', 'UINT16'],
                    ['Message ID', 'UINT16'],
                    ['Source ID', 'UINT32'],
                    ['Timestamp', 'UINT32'],
                    ['Reserved', 'UINT32'],
                    ['Reserved', 'UINT32'],
                    ['Reserved', 'UINT32'],
                    ['Reserved', 'UINT32'],
                    ['Scan Start(ps)', 'INT32'],
                    ['Scan Stop(ps)', 'INT32'],
                    ['Scan Step (bins)', 'INT16'],
                    ['Scan Type', 'UINT8'],
                    ['Reserved', 'UINT8'],
                    ['Antenna ID', 'UINT8'],
                    ['Operational Mode', 'UINT8'],
                    ['Number of Samples in message', 'UINT16'],
                    ['Number of samples total', 'UINT32'],
                    ['Message index', 'UINT16'],
                    ['Number of messages total', 'UINT16'],
                    ['Scan Data', 'INT32']
                    )
ENCODER_LIST = [ENCODER, DECODER, ENCODER31, DECODER32, ENCODER33, DECODER34, ENCODER35, DECODER36]
num_of_msg = ((scan_end - scan_start) // (61 * 350)) + 1
print("num of messages", num_of_msg)
for r in range(scanAmt * num_of_msg):
    ENCODER_LIST.append(DECODER21)

message_portion = []

for e in ENCODER_LIST:
    if isinstance(e, Encoder):
        e.send_message()
    elif isinstance(e, Decoder):
        message = e.receive_message(4096)
        if e is DECODER21:
            #print(message)
            if message['Message index'] < num_of_msg - 1:
                for sn in message['Scan Data']:
                    message_portion.append(sn)
            else: # message index == # of total messages
                for sn in message['Scan Data']:
                    message_portion.append(sn)
                data_array.append(message_portion)
                print(len(message_portion))
                message_portion = []

np.save("array_as_numpy.npy", np.array(data_array, dtype=float), allow_pickle=True)

'''
print(data_array)

list_of_files = glob.glob('../emulator/output/*')
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

with open('..\\emulator\\output\\20220719T102027_5_point_scatter_platform_pos.pkl', 'rb') as f:
    positions = pickle.load(f)

c = 299792458 #m/s
t = 0.017 * scanAmt # s

print(positions)

delta_pos = positions['platform_pos'][0,0] - positions['platform_pos'][scanAmt - 1,0]
v = abs(delta_pos / t)
wavelength = c / (4.3 * 10**9)
range_from_plane = math.sqrt((positions['platform_pos'][0,0] - 10)**2 + (positions['platform_pos'][0,1] - 10)**2 + (positions['platform_pos'][0,2])**2)

range_resolution = c / (2 * 1.1 * 10**9)
cross_range_resolution = (wavelength * range_from_plane) / (2 * v * t)

print(range_resolution)
print(cross_range_resolution)


np.save("array_as_numpy.npy", np.array(data_array, dtype=float), allow_pickle=True)

time = 0
times = []

full_array = np.add(np.array(data_array[0], dtype=float), np.array(data_array[1], dtype=float), np.array(data_array[2], dtype=float))

for i in range(len(full_array)):
    times += [time]
    time += int(32 * 1.907)



plt.subplot(211)
plt.plot(times, full_array)
plt.xlabel('Time (ps)')
plt.ylabel('Amplitude')


time = 0
times2 = []

for i in range(len(data_array[1])):
    times2 += [time]
    time += int(32 * 1.907)

plt.subplot(212)
plt.plot(times2, data_array[1])
plt.xlabel('Time (ps)')
plt.ylabel('Amplitude')
plt.show()

'''