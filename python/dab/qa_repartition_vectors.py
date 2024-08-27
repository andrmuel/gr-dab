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

from gnuradio import gr, gr_unittest, blocks
import dab_python as grdab


class qa_repartition_vectors(gr_unittest.TestCase):
    """
    @brief QA for the vector repartitioning block

    This class implements a test bench to verify the corresponding C++ class.
    """

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_repartition_vectors(self):
        ilen = 3
        mult = 2
        div = 3
        olen = 2
        src_data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6)
        trig =     (0,       1,       0,       0,          0,          0,       0,       0,       1,        1,       0      )
        expected_data = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 1, 2, 3, 4, 5, 6)
        expected_trig = (1,    0,    0,    0,      0,      0,      0,    0,    0,    1,    0,    0   )
        src = blocks.vector_source_b(src_data)
        trigsrc = blocks.vector_source_b(trig)
        s2v = blocks.stream_to_vector(gr.sizeof_char, ilen)
        repartition_vectors = grdab.repartition_vectors(gr.sizeof_char, ilen, olen, mult, div)
        v2s = blocks.vector_to_stream(gr.sizeof_char, olen)
        dst = blocks.vector_sink_b()
        trigdst = blocks.vector_sink_b()
        self.tb.connect(src, s2v, repartition_vectors, v2s, dst)
        self.tb.connect(trigsrc, (repartition_vectors, 1), trigdst)
        self.tb.run()
        result_data = dst.data()
        result_trig = trigdst.data()
        self.assertEqual(expected_data, result_data)
        self.assertEqual(expected_trig, result_trig)

    def test_002_repartition_vectors(self):
        ilen = 3
        mult = 2
        div = 3
        olen = 2
        src_data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6)
        trig =     (1,       0,       0,       0,          0,          0,       0,       0,       1,        1,       0      )
        expected_data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6)
        expected_trig = (1,    0,    0,    0,      0,      0,      0,    0,    0,    0,    0,    0,    1,    0,    0,  )
        src = blocks.vector_source_b(src_data)
        trigsrc = blocks.vector_source_b(trig)
        s2v = blocks.stream_to_vector(gr.sizeof_char, ilen)
        repartition_vectors = grdab.repartition_vectors(gr.sizeof_char, ilen, olen, mult, div)
        v2s = blocks.vector_to_stream(gr.sizeof_char, olen)
        dst = blocks.vector_sink_b()
        trigdst = blocks.vector_sink_b()
        self.tb.connect(src, s2v, repartition_vectors, v2s, dst)
        self.tb.connect(trigsrc, (repartition_vectors, 1), trigdst)
        self.tb.run()
        result_data = dst.data()
        result_trig = trigdst.data()
        self.assertEqual(expected_data, result_data)
        self.assertEqual(expected_trig, result_trig)

    def test_003_repartition_vectors(self):
        ilen = 3
        mult = 4
        div = 5
        olen = 2
        src_data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6)
        trig =     (1,       0,       0,       0,          1,          0,       0,       0,       1,        0,       0      )
        expected_data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5 )
        expected_trig = (1,    0,    0,    0,    0,     1,      0,     0,    0,    0,   )
        src = blocks.vector_source_b(src_data)
        trigsrc = blocks.vector_source_b(trig)
        s2v = blocks.stream_to_vector(gr.sizeof_char, ilen)
        repartition_vectors = grdab.repartition_vectors(gr.sizeof_char, ilen, olen, mult, div)
        v2s = blocks.vector_to_stream(gr.sizeof_char, olen)
        dst = blocks.vector_sink_b()
        trigdst = blocks.vector_sink_b()
        self.tb.connect(src, s2v, repartition_vectors, v2s, dst)
        self.tb.connect(trigsrc, (repartition_vectors, 1), trigdst)
        self.tb.run()
        result_data = dst.data()
        result_trig = trigdst.data()
        self.assertEqual(expected_data, result_data)
        self.assertEqual(expected_trig, result_trig)

if __name__ == '__main__':
    gr_unittest.main()
