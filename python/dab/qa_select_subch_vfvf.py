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

class qa_select_subch_vfvf (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_select_vectors(self):
        vlen_in = 2
        vlen_out = 6
        total_size = 8
        address = 1
        src_data = (
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        expected_data = (2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7)
        src = blocks.vector_source_f(src_data)
        s2v = blocks.stream_to_vector(gr.sizeof_float, vlen_in)
        select_subch = grdab.select_subch_vfvf(vlen_in, vlen_out, address, total_size)
        v2s = blocks.vector_to_stream(gr.sizeof_float, vlen_out)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, s2v, select_subch, v2s, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertFloatTuplesAlmostEqual2(result_data, expected_data)

    def test_002_select_vectors(self):
        vlen_in = 2
        vlen_out = 10
        total_size = 10
        address = 3
        src_data = (
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 0)
        expected_data = (6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        src = blocks.vector_source_f(src_data)
        s2v = blocks.stream_to_vector(gr.sizeof_float, vlen_in)
        select_subch = grdab.select_subch_vfvf(vlen_in, vlen_out, address, total_size)
        v2s = blocks.vector_to_stream(gr.sizeof_float, vlen_out)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, s2v, select_subch, v2s, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertFloatTuplesAlmostEqual2(result_data, expected_data)

    def test_003_select_vectors(self):
        vlen_in = 4
        vlen_out = 4
        total_size = 1
        address = 0
        src_data = (
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
            12, 13, 14, 15, 16, 17, 18, 19)
        expected_data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
            12, 13, 14, 15, 16, 17, 18, 19)
        src = blocks.vector_source_f(src_data)
        s2v = blocks.stream_to_vector(gr.sizeof_float, vlen_in)
        select_subch = grdab.select_subch_vfvf(vlen_in, vlen_out, address, total_size)
        v2s = blocks.vector_to_stream(gr.sizeof_float, vlen_out)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, s2v, select_subch, v2s, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertFloatTuplesAlmostEqual2(result_data, expected_data)

if __name__ == '__main__':
    gr_unittest.run(qa_select_subch_vfvf, "qa_select_subch_vfvf.xml")
