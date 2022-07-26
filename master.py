from classes import Encoder, Decoder, PORT, SIZES, data_array
import matplotlib.pyplot as plt
import numpy as np
import json
import sys
import itertools

DEFAULT_CONFIG = './image1_config.json'
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
                ['Message ID',  'UINT16',    0],
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
                ['Message ID', 'UINT16',   1],
                ['Node ID', 'UINT32', 1],
                ['Scan Start (ps)', 'INT32', scan_start],
                ['Scan End (ps)', 'INT32', scan_end],
                ['Scan Resolution (bins)', 'UINT16', 32], #DONT CHANGE
                ['Base Integration Index', 'UINT16', BII],
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
                    ['Message ID', 'UINT16', 2])

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
                ['Message ID', 'UINT16', 3],
                ['Scan Count', 'UINT16', scanAmt],
                ['Reserved', 'UINT16', 3],
                ['Scan Interval Time', 'UINT32', 0]
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
num_of_msg = int((scan_end - scan_start) // (61.024 * 350)) + 1
print("num of messages", num_of_msg)
for r in range(scanAmt * num_of_msg):
    ENCODER_LIST.append(DECODER21)

#Creates empty zero list length of the entire message and fills the zeroes with appropriate
#scanInfo according to messageID at the correct location. Sub messages that are dropped are 
#left as zeroes. 

#sacred

count = 0 # A helper Variable to set up everything
timeDelay = -1 #The calculated Delay between a set of scan messages
firstTime = -1 #The first timestamp of the scans
secondTime = -1 #The next set of scans timestamp
for e in ENCODER_LIST:
    if isinstance(e, Encoder):
        e.send_message()
    elif isinstance(e, Decoder):
        message = e.receive_message(4096)
        if message is None:
            break
        if e is DECODER21:
            if count == 0: #Initialize 2D Array and set firstTime
                finalArray = [[0]*message['Number of samples total'] for n in range(scanAmt)]
                firstTime = message['Timestamp']
                offset = message['Message index'] * 350
                finalArray[0][offset:(offset + message['Number of Samples in message'])] = message['Scan Data']
                count += 1
            if message['Timestamp'] == firstTime: #filling first row since we do not know second timestamp
                offset = message['Message index'] * 350
                finalArray[0][offset:(offset + message['Number of Samples in message'])] = message['Scan Data']
            if firstTime != message['Timestamp'] and count == 1: #Set second time when receiving the next timestamp
                secondTime = message['Timestamp']
                timeDelay = secondTime - firstTime
                offset = message['Message index'] * 350
                finalArray[(message['Timestamp'] - firstTime) // timeDelay][offset:(offset + message['Number of Samples in message'])] = message['Scan Data']
                count += 1
            else: # all other cases past first array and first scan of second array
                offset = message['Message index'] * 350
                finalArray[(message['Timestamp'] - firstTime) // timeDelay][offset:(offset + message['Number of Samples in message'])] = message['Scan Data']

               


#message_dict[message['Message ID']] = message
np.save("array_as_numpy.npy", np.array(finalArray, dtype=float), allow_pickle=True)


'''
all_msgs.append(message)

all_msgs.sort(key=lambda x: x["Message ID"])
all_ids = [x["Message ID"] for x in all_msgs]


total_expected_packets = all_msgs[0]["Number of messages total"]

print(total_expected_packets)
print('excess', (max(all_ids) % total_expected_packets))
missing_ids = set(range(max(all_ids))) - set(all_ids)
missing_ids = missing_ids - set(range(36))
# max(all_ids) does not care about dropped packet at the end
print('Missing ids', missing_ids)
former_timestamp = 0
current_timestamp = 0
data = []
counter = 3
current_scan = []
from functools import reduce
for i, msg in enumerate(all_msgs):
    
    
    if counter in missing_ids:
        if counter % total_expected_packets == 0:
            current_scan.append([0]*len(all_msgs[total_expected_packets - 1]["Scan Data"]))
        else:
        # we want to append a list of 0s the same length as the corresponding data in the first scan (maybe bugged)
            current_scan.append([0]*350)
    else:
        current_scan.append(msg["Scan Data"])
    
    # check if we are on a new scan
    if msg['Message index'] == total_expected_packets - 1:
            
        # current_scan = list(itertools.chain.from_iterable(current_scan))
        # crush the data into one list to represent scan

        current_scan = reduce(lambda x, y: x + y, current_scan)
        print(len(current_scan))
        data.append(current_scan)
        current_scan = []
    
    counter += 1
    former_timestamp = current_timestamp
'''