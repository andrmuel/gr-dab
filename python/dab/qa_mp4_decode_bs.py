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
from gnuradio import audio
import os
import dab_python as grdab

class qa_mp4_decode_bs (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

# manual check, if header info makes sense, and if audio is played, input = repaired (= Reed-Solomon decoded) DAB+ audio superframes
    def test_001_t (self):
        if os.path.exists("debug/reed_solomon_repaired.dat"):
            self.src = blocks.file_source_make(gr.sizeof_char, "debug/reed_solomon_repaired.dat")
            self.mp4 = grdab.mp4_decode_bs_make(14)
            self.s2f_left = blocks.short_to_float_make(1, 32767)
            self.s2f_right = blocks.short_to_float_make(1, 32767)
            self.audio = audio.sink_make(32000)

            self.tb.connect(self.src, (self.mp4, 0), self.s2f_left, (self.audio, 0))
            self.tb.connect((self.mp4, 1), self.s2f_right, (self.audio, 1))
            self.tb.run()
        else:
            log = gr.logger("log")
            log.debug("debug file not found - skipped test")
            log.set_level("WARN")
        pass


if __name__ == '__main__':
    gr_unittest.run(qa_mp4_decode_bs, "qa_mp4_decode_bs.xml")
