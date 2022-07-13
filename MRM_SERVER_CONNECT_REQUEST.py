from classes import Encoder, Decoder
SETTINGS_HEADER = 0x1004
ENCODER_37 = Encoder(['Settings Header', 'UINT16', 0x1004],
                ['Message ID', 'UINT16', 1],
                ['MRM IP Address', 'UINT32', 2],
                ['MRM IP Port', 'UINT16', 3],
                ['Reserved', 'UINT16', 4])

DECODER_38 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )
