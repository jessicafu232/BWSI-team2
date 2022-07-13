from commcheck import Encoder
import socket

PORT = 21210
SETTINGS_HEADER = 0x1001
SIZES = {
    'UINT8': 1,
    'UINT16': 2,
    'UINT32' : 4,
    'INT8': 1,
    'INT16': 2,
    'INT32' : 4,
    'CHAR[15]' : 15
}

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
serverAddressPort = ('localhost', PORT)
bufferSize = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
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
