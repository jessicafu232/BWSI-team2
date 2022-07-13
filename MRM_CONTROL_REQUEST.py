from classes import Encoder, Decoder, PORT, SIZES
import socket

ENCODER = Encoder(['Settings Header', 'UINT16', 0x1003],
                ['Message ID', 'UINT16', 1],
                ['Scan Count', 'UINT16', 1],
                ['Reserved', 'UINT16', 3],
                ['Scan Interval Time', 'UINT32', 10]
                )
bytesToSend = ENCODER.convert_to_bytes()
print(bytesToSend)
serverAddressPort  = ('localhost', PORT)
bufferSize = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPClientSocket.sendto(bytesToSend, serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)
msgFromServer = msgFromServer[0]

DECODER = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )
print(DECODER.decode(msgFromServer))