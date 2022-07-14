from classes import Encoder, Decoder, PORT, SIZES
import socket

ENCODER31 = Encoder(['Settings Header', 'UINT16', 0x1001],
                ['Message ID', 'UINT16', 1],
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
                    ['Message ID', 'UINT16', 37])

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
                ['Message ID', 'UINT16', 1],
                ['Scan Count', 'UINT16', 1],
                ['Reserved', 'UINT16', 3],
                ['Scan Interval Time', 'UINT32', 10]
                )

DECODER36 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )

ENCODER37 = Encoder(['Settings Header', 'UINT16', 0x1004],
                ['Message ID', 'UINT16', 1],
                ['MRM IP Address', 'UINT32', 2], # BIG PROBLEM: IP ADDRESS??
                ['MRM IP Port', 'UINT16', 21210],
                ['Reserved', 'UINT16', 4])

DECODER38 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )

ENCODER39 = Encoder(['Settings Header', 'UINT16', 0x1005],
                ['Message ID', 'UINT16', 1])

DECODER310 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )

ENCODER311 = Encoder(['Settings Header', 'UINT16', 0x1006],
                ['Message ID', 'UINT16', 1],
                ['Filter Mask', 'UINT16', 1],
                ['Motion Filter Index', 'UINT8', 1],
                ['Reserved', 'UINT8', 3]
                )

DECODER312 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )

ENCODER313 = Encoder(['Settings Header', 'UINT16', 0x1007],
                    ['Message ID', 'UINT16', 3])

DECODER314 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Filter Mask', 'UINT16'],
                ['Motion Filter Index', 'UINT8'],
                ['Reserved', 'UINT8'],
                ['Status', 'UINT32'])


ENCODER_LIST = [ENCODER31, DECODER32, ENCODER33, DECODER34, ENCODER35, DECODER36, ENCODER39, DECODER310, ENCODER311, DECODER312, ENCODER313, DECODER314]

TIMEOUT = 2 # the time in seconds the socket will wait for data from the server

serverAddressPort  = ('localhost', PORT)
bufferSize = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(TIMEOUT)
for e in ENCODER_LIST:
    if isinstance(e, Encoder): # check if encoder
        bytesToSend = e.convert_to_bytes()
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        msgFromServer = UDPClientSocket.recvfrom(bufferSize) # problem?
        msg = "Message from Server {}".format(msgFromServer[0])
        print(msg)
        msgFromServer = msgFromServer[0]
    else:
        print(e.decode(msgFromServer)) # decoder