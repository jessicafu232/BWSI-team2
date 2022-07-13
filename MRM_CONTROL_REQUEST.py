from classes import Encoder, Decoder

ENCODER = Encoder(['Settings Header', 'UINT16', 0x1003],
                ['Message ID', 'UINT16', 1],
                ['Scan Count', 'UINT16', 1],
                ['Reserved', 'UINT16', 3],
                ['Scan Interval Time', 'UINT32', 10]
                )

DECODER = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )
