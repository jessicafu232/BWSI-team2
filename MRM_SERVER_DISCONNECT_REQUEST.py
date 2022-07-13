from classes import Encoder, Decoder, PORT, SIZES
import socket
SETTINGS_HEADER = 0x1005
ENCODER_39 = Encoder(['Settings Header', 'UINT16', 0x1005],
                ['Message ID', 'UINT16', 1])
bytesToSend = ENCODER_39.convert_to_bytes()
serverAddressPort  = ('localhost', PORT)
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
msgFromServer = UDPClientSocket.recvfrom(bufferSize) # problem?
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)
msgFromServer = msgFromServer[0]

DECODER_310 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )
print(DECODER_310.decode(msgFromServer))
# assert isinstance(msgFromServer, bytearray)
# bytearray.decode(msgFromServer
