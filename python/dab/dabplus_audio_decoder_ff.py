#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, blocks
from gnuradio import filter
import gnuradio.dab as grdab

class dabplus_audio_decoder_ff(gr.hier_block2):
    """
    Hier block for decoding dab+ audio frames out of whole DAB transmission frame
    containing the following blocks:
    -msc_decode: extract subchannel and decode it
    -firecode checker
    -Reed Solomon error repair
    -mp4 decoder
    See the single blocks for more details
    """

    def __init__(self, dab_params, bit_rate, address, subch_size, protection, output_float, verbose=False, debug=False):
        if output_float: # map short samples to the range [-1,1] in floats
            gr.hier_block2.__init__(self,
                                    "dabplus_audio_decoder_ff",
                                    # Input signature
                                    gr.io_signature(1, 1, gr.sizeof_float * dab_params.num_carriers * 2),
                                    # Output signature
                                    gr.io_signature2(2, 2, gr.sizeof_float, gr.sizeof_float))
        else: # output signed 16 bit integers (directly from decoder)
            gr.hier_block2.__init__(self,
                                    "dabplus_audio_decoder_ff",
                                    # Input signature
                                    gr.io_signature(1, 1, gr.sizeof_float * dab_params.num_carriers * 2),
                                    # Output signature
                                    gr.io_signature2(2, 2, gr.sizeof_short, gr.sizeof_short))
        self.dp = dab_params
        self.bit_rate_n = bit_rate / 8
        self.address = address
        self.size = subch_size
        self.protection = protection
        self.output_float = output_float
        self.verbose = verbose
        self.debug = debug

        # sanity check
        # if self.bit_rate_n*6 != self.size:
        #     log = gr.logger("log")
        #     log.debug("bit rate and subchannel size are not fitting")
        #     log.set_level("ERROR")
        #     raise ValueError

        # MSC decoder extracts logical frames out of transmission frame and decodes it
        self.msc_decoder = grdab.msc_decode(self.dp, self.address, self.size, self.protection, self.verbose, self.debug)
        # firecode synchronizes to superframes and checks
        self.firecode = grdab.firecode_check_bb_make(self.bit_rate_n)
        # Reed-Solomon error repair
        self.rs = grdab.reed_solomon_decode_bb_make(self.bit_rate_n)
        # mp4 decoder
        self.mp4 = grdab.mp4_decode_bs_make(self.bit_rate_n)

        self.connect((self, 0), self.msc_decoder, self.firecode, self.rs, self.mp4)

        if self.output_float:
            # map short samples to the range [-1,1] in floats
            self.s2f_left = blocks.short_to_float_make(1, 32767)
            self.s2f_right = blocks.short_to_float_make(1, 32767)
            self.gain_left = blocks.multiply_const_ff(1, 1)
            self.gain_right = blocks.multiply_const_ff(1, 1)
            self.connect((self.mp4, 0), self.s2f_left, self.gain_left, (self, 0))
            self.connect((self.mp4, 1), self.s2f_right, self.gain_right, (self, 1))
        else:
            # output signed 16 bit integers (directly from decoder)
            self.connect((self.mp4, 0), (self, 0))
            self.connect((self.mp4, 1), (self, 1))

    def set_volume(self, volume):
        self.gain_left.set_k(volume)
        self.gain_right.set_k(volume)

    def get_sample_rate(self):
        return self.mp4.get_sample_rate()

    def get_firecode_passed(self):
        return self.firecode.get_firecode_passed()

    def get_corrected_errors(self):
        return self.rs.get_corrected_errors()
