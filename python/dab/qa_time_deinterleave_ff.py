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

class qa_time_deinterleave_ff (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t(self):
        vector01 =          (1, 0, 3, 0, 5, 0,   7, 2, 9, 4, 11, 6,   13, 8, 15, 10, 17, 12)
        expected_result =   (0, 0, 0, 0, 0, 0,   1, 2, 3, 4,  5, 6,    7, 8,  9, 10, 11, 12)
        src = blocks.vector_source_b(vector01, True)
        b2f = blocks.char_to_float()
        s2v = blocks.stream_to_vector(gr.sizeof_float, 6)
        time_deinterleaver = grdab.time_deinterleave_ff(6, [0, 1])
        v2s = blocks.vector_to_stream(gr.sizeof_float, 6)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, b2f, time_deinterleaver, blocks.head(gr.sizeof_float, 6*3), dst)
        self.tb.run()
        result = dst.data()
        #print result
        self.assertEqual(expected_result, result)

    def test_002_t(self):
        vector01 =          (1, 0, 0, 0,  5, 4, 0, 0,  9, 8, 3, 0,  13, 12, 7, 2)
        expected_result =   (0, 0, 0, 0,  0, 4, 0, 0,  0, 8, 0, 0,   1, 12, 3, 0)
        src = blocks.vector_source_b(vector01, True)
        b2f = blocks.char_to_float()
        s2v = blocks.stream_to_vector(gr.sizeof_float, 4)
        time_deinterleaver = grdab.time_deinterleave_ff(4, [0, 3, 2, 1])
        v2s = blocks.vector_to_stream(gr.sizeof_float, 4)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, b2f, time_deinterleaver, blocks.head(gr.sizeof_float, 4*4), dst)
        self.tb.run()
        result = dst.data()
        #print result
        self.assertEqual(expected_result, result)

    def test_003_t(self):
        vector01 =          (3, 0, 0, 0, 7, 0, 0, 0,    11, 4, 0, 0, 15, 8,  0, 0,      19, 12, 1, 0, 23, 16, 5, 0,     27, 20,  9,  2, 31, 24, 13,  6)
        expected_result =   (0, 0, 0, 0, 0, 0, 0, 0,     3, 4, 0, 0,  7, 8,  0, 0,      11, 12, 0, 0, 15, 16, 0, 0,      19,20, 0, 0, 23, 24, 0, 0)
        src = blocks.vector_source_b(vector01, True)
        b2f = blocks.char_to_float()
        s2v = blocks.stream_to_vector(gr.sizeof_float, 8)
        time_deinterleaver = grdab.time_deinterleave_ff(8, [2, 3, 0, 1])
        v2s = blocks.vector_to_stream(gr.sizeof_float, 8)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, b2f, time_deinterleaver, blocks.head(gr.sizeof_float, 8*4), dst)
        self.tb.run()
        result = dst.data()
        #print result
        self.assertEqual(expected_result, result)

    def test_004_t(self):
        vector01 =          (1, 2, 3, 4,  5, 6, 7, 8,  9, 10, 11, 12,  13, 14, 15, 16)
        expected_result =   (0,0,0,4,0,0,0,8,0,0,0,12,0,0,0,16,0,0,3,4,0,0,7,8,0,0,11,12,0,0,15,16)
        src = blocks.vector_source_b(vector01, True)
        b2f = blocks.char_to_float()
        s2v = blocks.stream_to_vector(gr.sizeof_float, 16)
        time_deinterleaver = grdab.time_deinterleave_ff(16, [0, 1, 2, 4])
        v2s = blocks.vector_to_stream(gr.sizeof_float, 16)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, b2f, time_deinterleaver, blocks.head(gr.sizeof_float, 16*2), dst)
        self.tb.run()
        result = dst.data()
        #print result
        self.assertEqual(expected_result, result)

if __name__ == '__main__':
    gr_unittest.run(qa_time_deinterleave_ff, "qa_time_deinterleave_ff.xml")
