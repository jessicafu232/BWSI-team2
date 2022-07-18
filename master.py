from classes import Encoder, Decoder, PORT, SIZES, data_array
import socket, struct
import matplotlib.pyplot as plt
import numpy as np

open('data.txt', 'w').close()
scanAmt = 3

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
                ['Scan Start (ps)', 'INT32', 23342],
                ['Scan End (ps)', 'INT32', 81935],
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
for r in range(scanAmt * 3):
    ENCODER_LIST.append(DECODER21)

message_portion = []

for e in ENCODER_LIST:
    if isinstance(e, Encoder):
        e.send_message()
    elif isinstance(e, Decoder):
        message = e.receive_message(4096)
        if e is DECODER21:
            if message['Message index'] < message['Number of messages total'] - 1:
                for sn in message['Scan Data']:
                    message_portion.append(sn)
            else:
                e.store_scan_info(message_portion)
                message_portion = []

print(data_array)

np.save("array_as_numpy.npy", np.array(data_array, dtype=float), allow_pickle=True)

time = 0
times = []

for i in range(len(data_array[0])):
    times += [time]
    time += int(32 * 1.907)

plt.plot(times, data_array[0])
plt.xlabel('Time (ps)')
plt.ylabel('Amplitude')
plt.show()