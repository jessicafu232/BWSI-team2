from classes import Encoder, Decoder
SETTINGS_HEADER = 0x1005
ENCODER_39 = Encoder(['Settings Header', 'UINT16', 0x1005],
                ['Message ID', 'UINT16', 1])

DECODER_310 = Decoder(['Settings Header', 'UINT16'],
                ['Message ID', 'UINT16'],
                ['Status', 'UINT32']
                )

