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

class Encoder:
    def __init__(self, *list):
        self.list = list
    '''Maybe some internal conversion to bytes? maybe a superclass to handle many messages in the future'''
    # this might be a stupid idea
    def convert_to_bytes(self):
        bytes = bytearray()
        for x in self.list:
            size = SIZES[x[1]]
            
            if 'U' in x[1]:
                if x[2] < 0:
                    raise ValueError('UNSIGNED INT IS NEGATIVE \n RECIEVED:', x[2])
                if x[2] > (2**(8*size)):
                    raise NameError('DATA TOO BIG') 
                for b in (int.to_bytes(x[2], size, 'big', signed=False)):
                    bytes.append(int(b))
            else:
                if x[2] > (2**(8*size-1)):
                    raise NameError('DATA TOO BIG') 
                for b in (int.to_bytes(x[2], size, 'big', signed=True)):
                    bytes.append(int(b))
        return bytes

class Decoder:
    def __init__(self, *list):
        self.list = list

    def decode(self, msgFromServer) -> dict:
        '''
            Tries to decode a bytearray from the server with the paridgm of the data
        '''
        start = 0
        recievedData = {}
        for i, sz in enumerate([x[1] for x in self.list]):
            end = start + SIZES[sz] 
            if sz == 'CHAR[15]':
                temp_byte = msgFromServer[start:end]
                temp_byte = '%' + str(temp_byte)[2:6] + '%' + str(temp_byte)[6:8] + '%' + str(temp_byte)[8:11] \
                + '%' + str(temp_byte)[11:13] + '%' + str(temp_byte)[13:15] + '%' + str(temp_byte)[15:]\

            elif sz in ['UINT8', 'UINT16', 'UINT32']:
                temp_byte = int.from_bytes(msgFromServer[start:end], 'big', signed=False)

            elif sz in ['INT8', 'INT16', 'INT32']:
                temp_byte = int.from_bytes(msgFromServer[start:end], 'big', signed=True)

            temp_dict = {self.list[i][0]:temp_byte}
            recievedData.update(temp_dict)
            start = end

        return recievedData

ENCODER = Encoder(['Settings Header', 'UINT16', 0xfffe],
                ['Message ID',  'UINT16',    86],
                ['uint8',       'UINT8',     69],
                ['uint16',      'UINT16',    420],
                ['uint32',      'UINT32',    69420],
                ['int8',        'INT8',      -69],
                ['int16',       'INT16',     -420],
                ['int32',       'INT32',     -69420]) 

bytesToSend = ENCODER.convert_to_bytes()
print(list(bytesToSend))
serverAddressPort = ('localhost', PORT)
bufferSize = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)
msgFromServer = msgFromServer[0]

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
print(DECODER.decode(msgFromServer))
