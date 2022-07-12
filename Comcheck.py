import socket

PORT = 21210
SETTINGS_HEADER = 0xfffe
SIZES = {
    'UINT8': 1,
    'UINT16': 2,
    'UINT32' : 4,
    'INT8': 1,
    'INT16': 2,
    'INT32' : 4,
}
class Message:
    def __init__(self, name:str, dtype:str, data):
        self.name = name
        self.dtype = dtype
        self.data = data
DATA = [Message('Hi', 'UINT16', 1829)]
serverAddressPort   = ('localhost', PORT)
bufferSize = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# 0xfffe is 0xff and 0xfe
bytesToSend = [0xff, 0xfe]
counter = 0
for types in DATA.keys():
    for i in range(SIZES[types]):
        bytesToSend.append(counter)
        counter += 1
bytesToSend = bytearray(bytesToSend)
print("HOST SENDING", bytesToSend)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)

msgFromServer = msgFromServer[0]
assert isinstance(msgFromServer, bytearray)
bytearray.decode(msgFromServer, )
