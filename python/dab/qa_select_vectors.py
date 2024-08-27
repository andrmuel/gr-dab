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


class qa_select_vectors(gr_unittest.TestCase):
    """
    @brief QA for the vector select block

    This class implements a test bench to verify the corresponding C++ class.
    """

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_select_vectors(self):
        skip = 2
        len = 3
        vlen = 2
        src_data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        trig =     (0,    1,    0,    0,    0,     0,      0,      0,     1,    1,    0,    0,    0   )
        expected_data = (6, 7, 8, 9, 10, 11, 6, 7, 8, 9)
        expected_trig = (1, 0, 0, 1, 0)
        src = blocks.vector_source_b(src_data)
        trigsrc = blocks.vector_source_b(trig)
        s2v = blocks.stream_to_vector(gr.sizeof_char, 2)
        select_vectors = grdab.select_vectors(gr.sizeof_char, vlen, len, skip)
        v2s = blocks.vector_to_stream(gr.sizeof_char, 2)
        dst = blocks.vector_sink_b()
        trigdst = blocks.vector_sink_b()
        self.tb.connect(src, s2v, select_vectors, v2s, dst)
        self.tb.connect(trigsrc, (select_vectors, 1), trigdst)
        self.tb.run()
        result_data = dst.data()
        result_trig = trigdst.data()
        # print expected_result
        # print result_data
        self.assertEqual(expected_data, result_data)
        self.assertEqual(expected_trig, result_trig)

    def test_002_select_vectors(self):
        skip = 2
        len = 3
        vlen = 2
        src_data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        trig =     (0,    1,    0,    0,    0,     0,      0,      0,     1,    1,    0,    0,    0   )
        expected_data = (6, 7, 8, 9, 10, 11, 6, 7, 8, 9)
        expected_trig = (1, 0, 0, 1, 0)
        src = blocks.vector_source_f(src_data)
        trigsrc = blocks.vector_source_b(trig)
        s2v = blocks.stream_to_vector(gr.sizeof_float, 2)
        select_vectors = grdab.select_vectors(gr.sizeof_float, vlen, len, skip)
        v2s = blocks.vector_to_stream(gr.sizeof_float, 2)
        dst = blocks.vector_sink_f()
        trigdst = blocks.vector_sink_b()
        self.tb.connect(src, s2v, select_vectors, v2s, dst)
        self.tb.connect(trigsrc, (select_vectors, 1), trigdst)
        self.tb.run()
        result_data = dst.data()
        result_trig = trigdst.data()
        # print expected_result
        # print result_data
        self.assertFloatTuplesAlmostEqual(expected_data, result_data)
        self.assertEqual(expected_trig, result_trig)

    def test_003_select_vectors(self):
        skip = 3
        len = 2
        vlen = 3
        src_data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        trig =     (1,       0,       0,       0,          0,          0,       0,       0,       1       )
        expected_data = (9, 10, 11, 12, 13, 14)
        expected_trig = (1,          0       )
        src = blocks.vector_source_f(src_data)
        trigsrc = blocks.vector_source_b(trig)
        s2v = blocks.stream_to_vector(gr.sizeof_float, vlen)
        select_vectors = grdab.select_vectors(gr.sizeof_float, vlen, len, skip)
        v2s = blocks.vector_to_stream(gr.sizeof_float, vlen)
        dst = blocks.vector_sink_f()
        trigdst = blocks.vector_sink_b()
        self.tb.connect(src, s2v, select_vectors, v2s, dst)
        self.tb.connect(trigsrc, (select_vectors, 1), trigdst)
        self.tb.run()
        result_data = dst.data()
        result_trig = trigdst.data()
        # print expected_result
        # print result_data
        self.assertFloatTuplesAlmostEqual(expected_data, result_data)
        self.assertEqual(expected_trig, result_trig)

    def test_004_select_vectors(self):
        skip = 3
        len = 3
        vlen = 3
        src_data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        trig =     (1,       1,       0,       0,          0,          0,       1,       0,       1       )
        expected_data = (12, 13, 14, 15, 0, 1)
        expected_trig = (1,           0      )
        src = blocks.vector_source_f(src_data)
        trigsrc = blocks.vector_source_b(trig)
        s2v = blocks.stream_to_vector(gr.sizeof_float, vlen)
        select_vectors = grdab.select_vectors(gr.sizeof_float, vlen, len, skip)
        v2s = blocks.vector_to_stream(gr.sizeof_float, vlen)
        dst = blocks.vector_sink_f()
        trigdst = blocks.vector_sink_b()
        self.tb.connect(src, s2v, select_vectors, v2s, dst)
        self.tb.connect(trigsrc, (select_vectors, 1), trigdst)
        self.tb.run()
        result_data = dst.data()
        result_trig = trigdst.data()
        # print expected_result
        # print result_data
        self.assertFloatTuplesAlmostEqual(expected_data, result_data)
        self.assertEqual(expected_trig, result_trig)

    def test_005_select_vectors(self):
        skip = 3
        len = 2
        vlen = 3
        src_data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        trig =     (1,       1,       0,       0,          1,          0,       1,       0,       0       )
        expected_data = ()
        expected_trig = ()
        src = blocks.vector_source_f(src_data)
        trigsrc = blocks.vector_source_b(trig)
        s2v = blocks.stream_to_vector(gr.sizeof_float, vlen)
        select_vectors = grdab.select_vectors(gr.sizeof_float, vlen, len, skip)
        v2s = blocks.vector_to_stream(gr.sizeof_float, vlen)
        dst = blocks.vector_sink_f()
        trigdst = blocks.vector_sink_b()
        self.tb.connect(src, s2v, select_vectors, v2s, dst)
        self.tb.connect(trigsrc, (select_vectors, 1), trigdst)
        self.tb.run()
        result_data = dst.data()
        result_trig = trigdst.data()
        # print expected_result
        # print result_data
        self.assertFloatTuplesAlmostEqual(expected_data, result_data)
        self.assertEqual(expected_trig, result_trig)

if __name__ == '__main__':
    gr_unittest.main()
