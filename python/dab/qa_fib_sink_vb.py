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
import dab_python as grdab

class qa_fib_sink_vb (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

#manual check of print outs with reference data of debug file (SWR radio station)
    def test_001_t (self):
        data = (
        0x05, 0x00, 0x10, 0xEA, 0x04, 0x24, 0x06, 0x02, 0xD3, 0xA6, 0x01, 0x3F, 0x06, 0xFF, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4C, 0x89)
        src = blocks.vector_source_b(data, True)
        fibout = blocks.stream_to_vector(1, 32)
        fibsink = grdab.fib_sink_vb()
        self.tb.connect(src, blocks.head(gr.sizeof_char, 300), fibout, fibsink)
        self.tb.run()
        pass

if __name__ == '__main__':
    gr_unittest.run(qa_fib_sink_vb, "qa_fib_sink_vb.xml")
