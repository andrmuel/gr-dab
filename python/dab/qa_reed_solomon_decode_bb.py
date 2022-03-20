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
import os

class qa_reed_solomon_decode_bb (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

# insert 5 errors in rs-encoded prbs reference sequence and correct them with rs_decoder
    def test_001_t(self):
        self.prbs = (
        154, 15, 22, 223, 146, 92, 238, 15, 39, 87, 230, 120, 80, 186, 147, 176, 169, 49, 253, 117, 245, 122, 30, 187,
        74, 141, 148, 1, 181, 10, 0, 244, 250, 199, 227, 56, 155, 105, 187, 219, 135, 61, 241, 87, 223, 75, 59, 112, 78,
        238, 63, 69, 246, 177, 92, 140, 117, 34, 254, 70, 18, 131, 116, 13, 51, 174, 239, 86, 135, 157, 180, 97, 156,
        48, 179, 190, 218, 99, 171, 29, 49, 42, 78, 63, 3, 7, 3, 145, 60, 180, 134, 27, 104, 230, 32, 171, 6, 109, 106,
        1, 6, 45, 104, 206, 138, 38, 107, 242, 128, 228)

        self.corrupted_data = (
        1, 1, 1, 1, 1, 92, 238, 15, 39, 87, 230, 120, 80, 186, 147, 176, 169, 49, 253, 117, 245, 122,
        30, 187, 74, 141, 148, 1, 181, 10, 0, 244, 250, 199, 227, 56, 155, 105, 187, 219, 135, 61,
        241, 87, 223, 75, 59, 112, 78, 238, 63, 69, 246, 177, 92, 140, 117, 34, 254, 70, 18, 131,
        116, 13, 51, 174, 239, 86, 135, 157, 180, 97, 156, 48, 179, 190, 218, 99, 171, 29, 49, 42,
        78, 63, 3, 7, 3, 145, 60, 180, 134, 27, 104, 230, 32, 171, 6, 109, 106, 1, 6, 45, 104,
        206, 138, 38, 107, 242, 128, 228, 215, 34, 43, 109, 122, 92, 195, 54, 105, 246)

        self.src = blocks.vector_source_b(self.corrupted_data)
        self.rs_decoder = grdab.reed_solomon_decode_bb_make(1)
        self.sink = blocks.vector_sink_b_make()
        self.tb.connect(self.src, self.rs_decoder, self.sink)
        self.tb.run()
        data = self.sink.data()
        self.assertEqual(data, self.prbs)


if __name__ == '__main__':
    gr_unittest.run(qa_reed_solomon_decode_bb, "qa_reed_solomon_decode_bb.xml")
