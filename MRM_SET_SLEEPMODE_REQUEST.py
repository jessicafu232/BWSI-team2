from classes import Encoder, Decoder

ENCODER = Encoder(['Settings Header', 'UINT16', 0xF005],
                ['Message ID', 'UINT16', 1],
                ['Sleep Mode', 'UINT32', 2]
                )

DECODER = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )
