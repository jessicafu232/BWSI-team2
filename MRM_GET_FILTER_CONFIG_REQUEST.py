from classes import Encoder, Decoder
#3.13 Encoder and Decoder
ENCODER313 = Encoder(['Settings Header', 'UINT 16', 0x1007],
                    ['Message ID', 'UINT16', 3])

DECODER34 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Filter Mask', 'INT8'],
                ['Reserved', 'UINT8'],
                ['Status', 'UINT32'])