from classes import Encoder, Decoder

ENCODER = Encoder(['Settings Header', 'UINT16', 0x1006],
                ['Message ID', 'UINT16', 1],
                ['Filter Mask', 'UINT16', 1],
                ['Motion Filter Index', 'UINT8', 1],
                ['Reserved', 'UINT8', 3]
                )

DECODER = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )
