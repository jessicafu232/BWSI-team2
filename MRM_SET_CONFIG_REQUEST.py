from commcheck import Encoder,Decoder, SIZES, PORT
SETTINGS_HEADER = 0x1001
ENCODER = Encoder(['Settings Header', 'UINT16', 0x1001],
                ['Message ID', 'UINT16', 1],
                ['Node ID', 'UINT16', 2],
                ['Scan Start (ps)', 'UINT16', 3],
                ['Scan End (ps)', 'UINT16', 5],
                ['Scan Resolution (bins)', 'UINT16', 7],
                ['Base Integration Index', 'UINT16', 11],
                ['Antenna Mode', 'UINT8', 13],
                ['Transmit Gain', 'UINT8', 17],
                ['Code Channel', 'UINT8', 19],
                ['Persist Flag', 'UNIT8', 23])
bytesToSend = ENCODER.convert_to_bytes()
print(list(bytesToSend))
serverAddressPort   = ('localhost', PORT)
bufferSize = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# 0xfffe is 0xff and 0xfe
# b = []
# for d in DATA:
#    b.append(d.convert_to_bytes())
# bytesToSend = bytearray(b)
# print("HOST SENDING", bytesToSend)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)
msgFromServer = msgFromServer[0]

DECODER = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Node ID', 'UINT16'],
                ['Scan Start (ps)', 'UINT16'],
                ['Scan End (ps)', 'UINT16'],
                ['Scan Resolution (bins)', 'UINT16'],
                ['Base Integration Index', 'UINT16'],
                ['Antenna Mode', 'UINT8'],
                ['Transmit Gain', 'UINT8'],
                ['Code Channel', 'UINT8'],
                ['Persist Flag', 'UNIT8']
)
print(DECODER.decode(msgFromServer))
# assert isinstance(msgFromServer, bytearray)
# bytearray.decode(msgFromServer, )
