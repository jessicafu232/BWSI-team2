from classes import Encoder, Decoder, PORT, SIZES
import socket

SETTINGS_HEADER = 0xfffe

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
