from classes import Encoder, Decoder

ENCODER = Encoder(['Settings Header', 'UINT16', 0xF003],
                ['Message ID', 'UINT16', 1],
                ['Operational Mode', 'UINT32', 1]
                )

DECODER = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Operational Mode', 'UINT32']
                ['Status', 'UINT32']
                )
