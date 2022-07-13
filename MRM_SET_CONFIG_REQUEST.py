from commcheck import Encoder, Decoder, SIZES, PORT
import socket

SETTINGS_HEADER = 0x1001
ENCODER = Encoder(['Settings Header', 'UINT16', 0x1001],
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
bytesToSend = ENCODER.convert_to_bytes()
print(list(bytesToSend))
serverAddressPort  = ('localhost', PORT)
bufferSize = 1024
print("kms")
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
print("1 i hate life")

# 0xfffe is 0xff and 0xfe
# b = []
# for d in DATA:
#    b.append(d.convert_to_bytes())
# bytesToSend = bytearray(b)
# print("HOST SENDING", bytesToSend)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
print("AAAA")
msgFromServer = UDPClientSocket.recvfrom(bufferSize) # problem?
print("a")
msg = "Message from Server {}".format(msgFromServer[0])
print("B")
print(msg)
msgFromServer = msgFromServer[0]

DECODER = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )
print(DECODER.decode(msgFromServer))
print("hm")
# assert isinstance(msgFromServer, bytearray)
# bytearray.decode(msgFromServer, )
