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

    def convert_to_bytes(self):
        #TODO
        pass

DATA = [
    Message('Settings Header', 'UINT16', 0xfffe),
    Message('uint8', 'UINT8', -69),
    Message('uint16', 'UINT16', -420),
    Message('uint32', 'UINT32', -69420),
    Message('int8', 'UINT8', 69),
    Message('int16', 'UINT16', 420),
    Message('int32', 'UINT32', 69420),
] 
serverAddressPort   = ('localhost', PORT)
bufferSize = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# 0xfffe is 0xff and 0xfe
b = []
for d in DATA:
    b.append(d.convert_to_bytes())
bytesToSend = bytearray(b)
print("HOST SENDING", bytesToSend)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)

msgFromServer = msgFromServer[0]
assert isinstance(msgFromServer, bytearray)
bytearray.decode(msgFromServer, )
