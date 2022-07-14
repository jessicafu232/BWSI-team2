PORT = 21210
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

            elif sz == 'CHAR[32]':
                charString = ""
                for a in msgFromServer[start:end]:
                    print(a)
                    charString = charString + str(a) + ", "
                temp_byte = charString

            elif sz in ['UINT8', 'UINT16', 'UINT32']:
                temp_byte = int.from_bytes(msgFromServer[start:end], 'big', signed=False)

            elif sz in ['INT8', 'INT16', 'INT32']:
                if recievedData.get('Settings Header') == 61953 and sz == 'INT32':
                    while end != len(msgFromServer):
                        temp_byte = int.from_bytes(msgFromServer[start:end], 'big', signed=True)
                        end = 
                else:
                    temp_byte = int.from_bytes(msgFromServer[start:end], 'big', signed=True)

            temp_dict = {self.list[i][0]:temp_byte}
            recievedData.update(temp_dict)
            start = end

        return recievedData
