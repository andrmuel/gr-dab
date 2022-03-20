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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import os
import dab_python as grdab

class qa_mp2_decode_bs (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

# test will be set up, when mp2 encoder is implemented
    def test_001_t (self):
        if os.path.exists("debug/mp2_encoded.dat"):
            self.src_mp2 = blocks.file_source_make(gr.sizeof_char, "debug/mp2_encoded.dat")
            self.unpack = blocks.packed_to_unpacked_bb_make(1, gr.GR_MSB_FIRST)
            self.mp2_decode = grdab.mp2_decode_bs_make(14)
            self.sink_left = blocks.file_sink_make(gr.sizeof_short, "debug/mp2_decoded_left.dat")
            self.sink_right = blocks.file_sink_make(gr.sizeof_short, "debug/mp2_decoded_right.dat")
            self.tb.connect(self.src_mp2, self.unpack, (self.mp2_decode, 0), self.sink_left)
            self.tb.connect((self.mp2_decode, 1), self.sink_right)
            self.tb.run()
        else:
            log = gr.logger("log")
            log.debug("debug file not found - skipped test")
            log.set_level("WARN")
        pass


if __name__ == '__main__':
    gr_unittest.run(qa_mp2_decode_bs, "qa_mp2_decode_bs.xml")
