from classes import Encoder, Decoder

ENCODER = Encoder(['Settings Header', 'UINT16', 0xF006],
                ['Message ID', 'UINT16', 1])
                

DECODER = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Sleep ID', 'UINT32']
                ['Status', 'UINT32']
                )
