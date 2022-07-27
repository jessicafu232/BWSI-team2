from classes import Encoder, Decoder
ENCODER33 = Encoder(['Settings Header', 'UINT 16', 0xF002],
                    ['Message ID', 'UINT16', 37])

DECODER34 = Decoder(['Settings Header', 'UINT16'],
                    ['Message ID', 'UINT16'])
