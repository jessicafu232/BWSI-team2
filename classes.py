from pyexpat.errors import messages
from turtle import goto
import socket, struct
import numpy as np

PORT = 21210
scanAmt = 50
SIZES = {
    'UINT8': 1,
    'UINT16': 2,
    'UINT32' : 4,
    'INT8': 1,
    'INT16': 2,
    'INT32' : 4,
    'CHAR[15]' : 15,
    'CHAR[32]' : 32
}

STATUSES = {1: 'STATUS 1: GENERIC FAILURE',
            2: 'STATUS 2: WRONG OP MODE',
            3: 'STATUS 3: UNSUPPORTED VALUE',
            4: 'STATUS 4: INVALID DURING SLEEP',
            5: 'STATUS 5: WRONG MESSAGE SIZE',
            6: 'STATUS 6: NOT ENABLED',
            7: 'STATUS 7: WRONG BUFFER SIZE',
            8: 'STATUS 8: UNRECOGNIZED MESSAGE TYPE'
}   

data_array = []

TIMEOUT = 10
serverAddressPort = ('localhost', PORT)
bufferSize = 4096
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(TIMEOUT)

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

    def send_message(self):
        #print('Sending: ', self.list)

        bytesToSend = self.convert_to_bytes()
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        return None

class Decoder:
    def __init__(self, *list):
        self.list = list
        self.message_portion = []

    def decode(self, msgFromServer) -> dict:
        '''
            Tries to decode a bytearray from the server with the paridgm of the data
        '''
        start = 0
        recievedData = {}
        data = []
        for i, sz in enumerate([x[1] for x in self.list]):
            end = start + SIZES[sz] 
            if sz == 'CHAR[15]':
                temp_byte = msgFromServer[start:end]
                temp_byte = '%' + str(temp_byte)[2:6] + '%' + str(temp_byte)[6:8] + '%' + str(temp_byte)[8:11] \
                + '%' + str(temp_byte)[11:13] + '%' + str(temp_byte)[13:15] + '%' + str(temp_byte)[15:]\

            elif sz == 'CHAR[32]':
                charString = ""
                for a in msgFromServer[start:end]:
                    charString = charString + str(a) + ", "
                temp_byte = charString

            elif sz in ['UINT8', 'UINT16', 'UINT32']:
                temp_byte = int.from_bytes(msgFromServer[start:end], 'big', signed=False)

            elif sz in ['INT8', 'INT16', 'INT32']:
                if recievedData.get('Settings Header') == 61953 and i == 19:
                    flag=True
                    while flag:
                        data.append(int.from_bytes(msgFromServer[start:end], 'big', signed=True))
                        flag = end < len(msgFromServer)
                        start = end
                        end = start + 4
                    temp_byte = data
                    # print(len(data))
                else:
                    temp_byte = int.from_bytes(msgFromServer[start:end], 'big', signed=True)

            temp_dict = {self.list[i][0]:temp_byte}
            recievedData.update(temp_dict)
            start = end
        return recievedData

    def receive_message(self, bufferSize=4096):
        #receives the message
        try:
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        except socket.timeout:
            return None

        msgFromServer = msgFromServer[0]
        #msg = "Message from Server {}".format(msgFromServer[0])
        message = self.decode(msgFromServer)
        #print("Message from Server: ", message)
        #checks the status to make sure its 0
        if message.get('Settings Header') != 61953:
            status = message['Status']
            if status != 0:
                raise ValueError('Message #' + str(message['Settings Header']) + ' ' + STATUSES[status])
            else:
                return message
        else:
            return message

    '''
    def store_scan_info(self, m):
        stores the scan info in a data.txt file

        data_array.append(m)
        with open('data.txt', 'a') as f:
                f.write(str(m))

        return None
    '''