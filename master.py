from classes import Encoder, Decoder, PORT, SIZES, data_array
import matplotlib.pyplot as plt
import numpy as np
import json
import sys

DEFAULT_CONFIG = './five_point_config.json'
if len(sys.argv) == 2:
    file = sys.argv[1]
else:
    file = DEFAULT_CONFIG
with open(file, 'r') as f:
    config = json.load(f)

scan_start = config['Scan start']
scan_end = config['Scan end']
scanAmt = config['Scan Amount']
BII = config['Base Integration Index']

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
                ['Scan Resolution (bins)', 'UINT16', 32], #DONT CHANGE
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
                ['Scan Interval Time', 'UINT32', 2000]
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
                    ['Number of Samples total', 'UINT32'],
                    ['Message index', 'UINT16'],
                    ['Number of messages total', 'UINT16'],
                    ['Scan Data', 'INT32']
                    )
ENCODER_LIST = [ENCODER, DECODER, ENCODER31, DECODER32, ENCODER33, DECODER34, ENCODER35, DECODER36]
num_of_msg = int((scan_end - scan_start) // (61.024 * 350)) + 1
print("num of messages", num_of_msg)
for r in range(scanAmt * num_of_msg):
    ENCODER_LIST.append(DECODER21)


#Creates empty zero list length of the entire message and fills the zeroes with appropriate
#scanInfo according to messageID at the correct location. Sub messages that are dropped are 
#left as zeroes. 
message_portion = []
count = 1
for e in ENCODER_LIST:
    if isinstance(e, Encoder):
        e.send_message()
    elif isinstance(e, Decoder):
        message = e.receive_message(4096)
        if message is None:
            break
        if e is DECODER21:
            if count == 1:
                message_portion = [0] * message['Number of Samples total']
                maximum = message['Number of messages total']
                offset = message['Message index'] * 350
                message_portion[offset:(offset + message['Number of Samples in message'])] = message['Scan Data']
                count += 1
            if count == maximum + 1:
                offset = message['Message index'] * 350
                message_portion[offset:(offset + message['Number of Samples in message'])] = message['Scan Data']
                count = 1
                data_array.append(message_portion)
                # print(message_portion)
                message_portion = []
            else: # message index is between 1 and the last index
                offset = message['Message index'] * 350
                message_portion[offset:(offset + message['Number of Samples in message'])] = message['Scan Data']
                count += 1

'''
                for sn in message['Scan Data']:
                    message_portion.append(sn)
                data_array.append(message_portion) 
                message_portion = []
            

        
           #'num samples total'     
'''

#message_dict[message['Message ID']] = message
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
