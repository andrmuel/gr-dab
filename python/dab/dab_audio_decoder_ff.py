#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 Ruben Undheim
# (based on code from Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).)
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

class dab_audio_decoder_ff(gr.hier_block2):
    """
    """

    def __init__(self, dab_params, bit_rate, address, subch_size, protection, output_float, verbose=False, debug=False):
        if output_float: # map short samples to the range [-1,1] in floats
            gr.hier_block2.__init__(self,
                                    "dab_audio_decoder_ff",
                                    # Input signature
                                    gr.io_signature(1, 1, gr.sizeof_float * dab_params.num_carriers * 2),
                                    # Output signature
                                    gr.io_signature2(2, 2, gr.sizeof_float, gr.sizeof_float))
        else: # output signed 16 bit integers (directly from decoder)
            gr.hier_block2.__init__(self,
                                    "dab_audio_decoder_ff",
                                    # Input signature
                                    gr.io_signature(1, 1, gr.sizeof_float * dab_params.num_carriers * 2),
                                    # Output signature
                                    gr.io_signature2(2, 2, gr.sizeof_short, gr.sizeof_short))

        self.msc_dec = grdab.msc_decode(dab_params, address, subch_size, protection)
        self.unpack = blocks.packed_to_unpacked_bb_make(1, gr.GR_MSB_FIRST)
        self.mp2_dec = grdab.mp2_decode_bs_make(bit_rate / 8)
        self.connect((self, 0), self.msc_dec, self.unpack, self.mp2_dec)

        if output_float:
            # map short samples to the range [-1,1] in floats
            self.s2f_left = blocks.short_to_float_make(1, 32767)
            self.s2f_right = blocks.short_to_float_make(1, 32767)
            self.gain_left = blocks.multiply_const_ff(1, 1)
            self.gain_right = blocks.multiply_const_ff(1, 1)
            self.connect((self.mp2_dec, 0), self.s2f_left, self.gain_left, (self, 0))
            self.connect((self.mp2_dec, 1), self.s2f_right, self.gain_right, (self, 1))
        else:
            # output signed 16 bit integers (directly from decoder)
            self.connect((self.mp2_dec, 0), (self, 0))
            self.connect((self.mp2_dec, 1), (self, 1))

    def set_volume(self, volume):
        self.gain_left.set_k(volume)
        self.gain_right.set_k(volume)

    def get_sample_rate(self):
        return self.mp2_dec.get_sample_rate()
