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
    'CHAR[15]' : 15
}


class Messages:
    def __init__(self, *list):
        self.list = list
    '''Maybe some internal conversion to bytes? maybe a superclass to handle many messages in the future'''
    # this might be a stupid idea
    def convert_to_bytes(self):
        bytes = bytearray()
        for x in self.list:
            size = SIZES[x[1]]
            if x[2] > (2**(8*size)):
                raise NameError('DATA TOO BIG') 
            if 'U' in x[1]:
                for b in (int.to_bytes(x[2], size, 'big', signed=False)):
                    bytes.append(int(b))
            else:
                for b in (int.to_bytes(x[2], size, 'big', signed=True)):
                    bytes.append(int(b))
        print(bytes)
        return bytes
DATA = Messages(['Settings Header', 'UINT16', 0xfffe],
    ['Message ID', 'UINT16', 86],
    ['uint8', 'UINT8', 69],
    ['uint16', 'UINT16', 420],
    ['uint32', 'UINT32', 69420],
    ['int8', 'INT8', -69],
    ['int16', 'INT16', -420],
    ['int32', 'INT32', -69420]) 
bytesToSend = DATA.convert_to_bytes()
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

DECODER = {
    'Settings Header': 2,
    'Message ID': 2,
    'UINT8': 1,
    'UINT163': 2,
    'UINT32' : 4,
    'INT8': 1,
    'INT16': 2,
    'INT32' : 4,
    'CHAR[15]' : 15,
    'Status': 4,
}

counter = 0

recievedData = {}

for sz in DECODER:
    farform = counter + DECODER.get(sz)
    if counter == 0 or sz == 'CHAR[15]':
        temp_byte = msgFromServer[counter:farform]
    #elif :
    #    temp_byte = str(msgFromServer[counter:farform][:4]) + "-" + str(msgFromServer[counter:farform][4:6]) + "-" + str(msgFromServer[counter:farform][7:9]) + "-"
    elif 'U' in sz:
        temp_byte = int.from_bytes(msgFromServer[counter:farform], 'big', signed=False)
    else:
        temp_byte = int.from_bytes(msgFromServer[counter:farform], 'big', signed=True)
    temp_dict = {sz:temp_byte}
    recievedData.update(temp_dict)
    counter = farform
print(recievedData)

# assert isinstance(msgFromServer, bytearray)
# bytearray.decode(msgFromServer, )