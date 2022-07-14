from classes import Encoder, Decoder, PORT, SIZES
import socket, struct
import numpy as np
ip_address = "127.0.0.1"

def ip2long(ip):
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

ip_address = ip2long(ip_address)
print(ip_address)

ip_address = 2130706433
scanAmt = 4
scanInfo = list()

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
                ['Node ID', 'UINT32', 2],
                ['Scan Start (ps)', 'INT32', 3],
                ['Scan End (ps)', 'INT32', 5],
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
                ['Transmit Gain', 'UINT8', 6],
                ['Code Channel', 'UINT8', 7],
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
                ['Scan Interval Time', 'UINT32', 10]
                )

DECODER36 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )

ENCODER37 = Encoder(['Settings Header', 'UINT16', 0x1004],
                ['Message ID', 'UINT16', 37],
                ['MRM IP Address', 'UINT32', ip_address], # BIG PROBLEM: IP ADDRESS??
                ['MRM IP Port', 'UINT16', 21210],
                ['Reserved', 'UINT16', 4])

DECODER38 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )

ENCODER39 = Encoder(['Settings Header', 'UINT16', 0x1005],
                ['Message ID', 'UINT16', 39])

DECODER310 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )

ENCODER311 = Encoder(['Settings Header', 'UINT16', 0x1006],
                ['Message ID', 'UINT16', 311],
                ['Filter Mask', 'UINT16', 1],
                ['Motion Filter Index', 'UINT8', 1],
                ['Reserved', 'UINT8', 3]
                )

DECODER312 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )

ENCODER313 = Encoder(['Settings Header', 'UINT16', 0x1007],
                ['Message ID', 'UINT16', 313])

DECODER314 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Filter Mask', 'UINT16'],
                ['Motion Filter Index', 'UINT8'],
                ['Reserved', 'UINT8'],
                ['Status', 'UINT32'])

ENCODER315 = Encoder(['Settings Header', 'UINT16', 0xF001],
                ['Message ID', 'UINT16', 315])

DECODER316 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['MRM Version Major', 'UINT8'],
                ['MRM Version Minor', 'UINT8'],
                ['MRM Version Build', 'UINT16'],
                ['UWB Kernel Major', 'UINT8'],
                ['UWB Kernel Minor', 'UINT8'],
                ['UWB Kernel Build', 'UINT16'],
                ['FPGA Firmware Version', 'UINT8'],
                ['FPGA Firmware Year', 'UINT8'],
                ['FPGA Firmware Month', 'UINT8'],
                ['FPGA Firmware Day', 'UINT8'],
                ['Serial Number', 'UINT32'],
                ['Board Revision', 'UINT8'],
                ['Power-On BIT Test Result', 'UINT8'],
                ['Board Type', 'UINT8'],
                ['Transmitter Configuration', 'UINT8'],
                ['Temp', 'INT32'],
                ['Package Version', 'CHAR[32]'],
                ['Status', 'UINT32'])

ENCODER317 = Encoder(['Settings Header', 'UINT16', 0xF002],
                ['Message ID', 'UINT16', 317])

DECODER318 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'])

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
                    ['Scan Data', 'INT32'])

ENCODER_LIST = [ENCODER, DECODER, ENCODER31, DECODER32, ENCODER33, DECODER34, ENCODER35, DECODER36]
for r in range(scanAmt):
    ENCODER_LIST.append(DECODER21)
ENCODER_LIST.append(ENCODER317)
ENCODER_LIST.append(DECODER318)

TIMEOUT = 2 # the time in seconds the socket will wait for data from the server

serverAddressPort  = ('localhost', PORT)
bufferSize = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(TIMEOUT)



for e in ENCODER_LIST:
    if isinstance(e, Encoder): # check if encoder
        bytesToSend = e.convert_to_bytes()
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        
     
    else:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize) # problem?
        msgFromServer = msgFromServer[0]  
        print(msgFromServer)
        msg = "Message from Server {}".format(msgFromServer[0])
        print(msg)
        print(e.decode(msgFromServer)) # decoder