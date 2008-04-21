# DAB parameters for mode I to IV
# see Table 38, page 145 of the DAB specification

# index starts at 1

symbols_per_frame = [-1,76, 76, 153, 76]         # OFDM symbols per frame (excl. NS)
carriers = [-1,1536, 384, 192, 768]              # number of carriers -> carrier width = 1536kHz/carriers
frame_length = [-1,196608, 49152, 49152, 98304]  # samples per frame; in ms: 96,24,24,48 (incl. NS)
ns_length = [-1,2656, 664, 345, 1328]            # length of null symbol in samples
symbol_length = [-1,2552, 638, 319, 1276]        # length of an OFDM symbol in samples
fft_length = [-1,2048, 512, 256, 1024]           # fft length
cp_length = [-1,504, 126, 63, 252]               # length of cyclic prefix

# sanity checks:
#
# symbols_per_frame*symbol_length+ns_length = frame_length
# symbol_length = fft_length+cp_length

default_sample_rate = 2048000
T = 1./default_sample_rate
